from datetime import timedelta
from django.db.models import Model
from django.http import HttpResponse, JsonResponse
from django.utils import timezone
from .serializers import *
from .models import User, Question, Meta, Card
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import generics, status
from knox.models import AuthToken
from rest_framework.response import Response
from django.contrib.auth import authenticate
import re
import hashlib

# @permission_classes([ AllowAny ])
# def social_generate_token(request):
#     if request.user.is_authenticated:
#         response = redirect('/')
#         response.set_cookie('token', AuthToken.objects.create(request.user)[1], expires=timezone.now() + timedelta(days=3))
#         return response
#     return HttpResponse('Not authenticated', status=status.HTTP_401_UNAUTHORIZED)


@permission_classes([AllowAny])
class sociallogin_get_token(generics.GenericAPIView):
    def post(self, request, *args, **kwargs):
        data = dict(request.data)
        if (
            (data.get("email") and
             data.get("email_verified") and
             data.get("family_name") and
             data.get("given_name") and
             data.get("name") and
             data.get("picture"))
                is None):
            return HttpResponse('Not authenticated', status=status.HTTP_401_UNAUTHORIZED)
        else:
            try:
                user = User.objects.get(email=data.get("email"))
            except User.DoesNotExist:
                user = User.objects.create(email=data.get(
                    "email"), first_name=data["given_name"], last_name=data["family_name"], picture=data["picture"], username=hashlib.md5(data["email"].encode()).hexdigest())
            return Response({
                "success": True,
                "token": AuthToken.objects.create(user)[1]
            })


@permission_classes([AllowAny])
def check_game_live(request):
    meta = Meta.objects.filter()[0]
    now = timezone.now()
    if now > meta.start_time:
        if now < meta.end_time:
            return JsonResponse({
                'game_live': True,
                'date': meta.end_time
            })
        return JsonResponse({
            'time_up': True,
            'game_live': False,
            'date': meta.end_time
        })

    return JsonResponse({
        'game_live': False,
        'date': meta.start_time
    })


@permission_classes([AllowAny])
def leaderboard(request):
    # try:
    leaderboard = list(User.objects.filter().order_by('-points', 'time'))

    # Tie breaker in case of same points
    # for i in range(len(leaderboard)):
    #     for j in range(i, len(leaderboard)):
    #         if leaderboard[i].points == leaderboard[j].points:
    #             if leaderboard[i].time > leaderboard[j].time:
    #                 leaderboard[i], leaderboard[j] = leaderboard[j], leaderboard[i]
    board = []
    for user in leaderboard:
        try:
            if user.first_name and user.last_name and user.picture:
                board.append({'username': user.username, 'name': user.first_name +
                              ' ' + user.last_name, 'points': user.points, "avatar": user.picture})
        except:
            continue

    return JsonResponse({
        'leaderboard': board
    })
    # except:
    #     return JsonResponse({
    #         'message': 'Server failed to process the request'
    #     }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@permission_classes([AllowAny,])
class register(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        if (
            request.data.get("username") != ""
            and request.data.get("password") != ""
        ):
            try:
                user = User.objects.create_user(
                    username=request.data.get("username"),
                    password=request.data.get("password")
                )
            except:
                return Response("Username already used!!", status=status.HTTP_400_BAD_REQUEST)
            return Response(
                {
                    "token": AuthToken.objects.create(user)[1],
                    "status": 200,
                }
            )
        return Response(
            "Username and password are required fields", status=status.HTTP_400_BAD_REQUEST
        )


@permission_classes([AllowAny,])
class login(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = authenticate(
            username=request.data.get("username"), password=request.data.get("password")
        )
        if user is not None:
            return Response(
                {
                    "user": LoginSerializer(
                        user, context=self.get_serializer_context()
                    ).data,
                    "token": AuthToken.objects.create(user)[1],
                    "status": 200,
                }
            )
        else:
            return Response(
                "Wrong Credentials! Please try again.", status=status.HTTP_403_FORBIDDEN
            )

 
@permission_classes(
    [IsAuthenticated]
)
class question(generics.GenericAPIView):
    def get(self, request):
        cround = request.user.current_round
        try:
            if cround > Question.objects.filter().count():
                return JsonResponse({
                    'gameOver': True,
                    'message': 'Game is over'
                })
            question = Question.objects.get(round=cround)
            try:
                media = question.media.url
            except ValueError:
                media = ''

            # To make sure that the wait_time is not reset everytime a
            # user fetches the question, for example when refreshing the page
            if request.user.calc_wait_time_from is None:
                request.user.calc_wait_time_from = timezone.now()
                request.user.save()

            return JsonResponse({
                'text': question.text,
                'round': question.round,
                'ogmedia': question.ogmedia,
                'year': question.year,
                'country': question.country,
                'language': question.language,
                'show_country': request.user.show_country,
                'show_media': request.user.show_media,
                'show_language': request.user.show_language,
                'show_year': request.user.show_year
            })
        except Model.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)


@permission_classes(
    [IsAuthenticated]
)
class clue(generics.GenericAPIView):
    def get(self, request):
        cround = request.user.current_round
        try:
            question = Question.objects.get(round=cround)
        except Question.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)

        # Make sure that enough time has passed for the user
        diff = timezone.now() - request.user.calc_wait_time_from
        print(timezone.now(), request.user.calc_wait_time_from, diff)
        if question.clue_wait_time < 0:
            return JsonResponse({
                'not-available': True,
                'success': True
            })
        if diff > timedelta(minutes=question.clue_wait_time):
            return JsonResponse({
                'clue': question.clue,
                'success': True
            })
        else:
            return JsonResponse({
                'message': f'Wait for {question.clue_wait_time * 60 - diff.seconds} more second(s) to view your clue.',
                'timeleft': question.clue_wait_time * 60 - diff.seconds,
                'success': False
            })


@permission_classes(
    [IsAuthenticated]
)
class checkClueAvailability(generics.GenericAPIView):
    def get(self, request):
        cround = request.user.current_round
        try:
            question = Question.objects.get(round=cround)
        except Question.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found',
                'success': False
            }, status=status.HTTP_404_NOT_FOUND)

        # Make sure that enough time has passed for the user
        diff = timezone.now() - request.user.calc_wait_time_from
        if question.clue_wait_time < 0:
            return JsonResponse({
                'not-available': True,
                'success': True
            })
        if diff > timedelta(minutes=question.clue_wait_time):
            return JsonResponse({
                'available': True,
                'success': True
            })
        else:
            return JsonResponse({
                'available': False,
                'timeleft': question.clue_wait_time * 60 - diff.seconds,
                'success': True
            })


@permission_classes(
    [IsAuthenticated]
)
class answer(generics.GenericAPIView):
    def post(self, request):
        cround = request.user.current_round

        if 'answer' not in request.data.keys():
            return JsonResponse({'message': 'Empty answer not accepted'}, status=status.HTTP_400_BAD_REQUEST)

        answer = request.data.get('answer').lower().strip()
        answer = re.sub(' +', ' ', answer)

        try:
            question = Question.objects.get(round=cround)
            if (len(question.answer.split(',')) > 1):
                if answer in question.answer.split(','):
                    # Increment points
                    request.user.current_round = cround + 1
                    #request.user.points += question.points
                    request.user.time = timezone.now()
                    request.user.calc_wait_time_from = None
                    request.user.cons_aval += question.coins
                    request.user.show_country = False
                    request.user.show_media = False
                    request.user.show_language = False
                    request.user.show_year = False

                    if(request.user.rf_start_time != None):
                        diff = timezone.now() - request.user.rf_start_time
                        if(diff > timedelta(minutes=5)):
                            request.user.rf_active = False
                            request.user.rf_start_time = None
                            request.user.points += question.points
                        else:
                            request.user.points += question.points*2

                    else:
                        request.user.points += question.points


                    request.user.save()
                    return JsonResponse({
                        'success': True
                    })
            if question.answer == answer:

                # Increment points
                request.user.current_round = cround + 1
                #request.user.points += question.points
                request.user.time = timezone.now()
                request.user.calc_wait_time_from = None
                request.user.coins_aval += question.coins
                request.user.show_country = False
                request.user.show_media = False
                request.user.show_language = False
                request.user.show_year = False
                
                if(request.user.rf_start_time != None):
                    diff = timezone.now() - request.user.rf_start_time
                    if(diff > timedelta(minutes=5)):
                        request.user.rf_active = False
                        request.user.rf_start_time = None
                        request.user.points += question.points
                    else:
                        request.user.points += question.points*2

                else:
                    request.user.points += question.points

                request.user.save()
                return JsonResponse({
                    'success': True
                })

            return JsonResponse({
                'success': False
            })
        except Model.DoesNotExist:
            return JsonResponse({
                'message': 'Question not found'
            }, status=status.HTTP_404_NOT_FOUND)

@permission_classes([IsAuthenticated])
class getCards(generics.GenericAPIView):
    def get(self, request):
        cards = list(Card.objects.filter())
        
        aval_cards = request.user.cardTypeA

        cardList = []
        for card in cards:
            try:
                cardList.append({'aval_cards': aval_cards, 'index': card.card_num, 'text': card.card_text, 'desc': card.card_desc, 'coins': card.card_coins})
            except:
                continue

        return JsonResponse({
            'cards': cardList
        })

@permission_classes([IsAuthenticated])
class changeCardStatus(generics.GenericAPIView):
    def post(self, request):

        aval_cards = request.user.cardTypeA
        current_status = aval_cards[request.data.get('index')]
        i = request.data.get('index')

        new_status = '0'
        if(current_status == '0'):
            if(request.user.coins_aval >= request.data.get('coins')):
                request.user.coins_aval = request.user.coins_aval - request.data.get('coins')
                new_status = '1'
        if(current_status == '1'):
            if(i == 0):
                user = User.objects.filter().order_by('-points', 'time')[:1].get()
                if(user.points >= 10):
                    user.points = user.points-10
                user.save()
            if(i == 1):
                request.user.points = request.user.points + 10
            if(i == 2):
                request.user.show_country = True
            if(i == 3):
                request.user.show_language = True
            if(i == 4):
                request.user.show_year = True
            if(i == 5):
                request.user.show_media = True
            if(i==6):
                request.user.current_round = request.user.current_round +1
                request.user.time = timezone.now()
                request.user.calc_wait_time_from = None
                request.user.show_country = False
                request.user.show_media = False
                request.user.show_language = False
                request.user.show_year = False
            if(i==7):
                request.user.rf_active = True
                request.user.rf_start_time = timezone.now()

        aval_cards = aval_cards[:i] + new_status + aval_cards[i+1:]
        request.user.cardTypeA = aval_cards
        
        request.user.save()
        
        print(User.objects.filter().order_by('-points', 'time')[:1].get().points)
        return JsonResponse({'success': True})

@permission_classes([IsAuthenticated])
class getUserCoins(generics.GenericAPIView):
    def get(self, request):
        coins = request.user.coins_aval
        return JsonResponse({
            'coins' : coins
        })
