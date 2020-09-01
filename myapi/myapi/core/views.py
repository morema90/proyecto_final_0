from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from django.urls import reverse_lazy
from . import serializers
from .forms import EventForm, UserForm
from .models import *
from rest_framework.permissions import IsAuthenticated
from django.http import Http404, HttpResponseRedirect, request
from rest_framework import status
from django.views.generic import TemplateView, FormView
from django.shortcuts import redirect, render
from .serializers import EventSerializer
from django.contrib.auth import logout as do_logout


class User(APIView, TemplateView):
    template_name = "Hoja2.html"

    def post(self, request):
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            return redirect('http://172.24.98.163:8080/api/events/list/')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.UserSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


class Login(FormView):
    template_name = "Hoja1.html"
    form_class = AuthenticationForm
    success_url = reverse_lazy("events_list")

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login, self).dispatch(request, *args, *kwargs)

    def form_valid(self, form):
        user = authenticate(
            username=form.cleaned_data['email'], password=form.cleaned_data['password'])
        token, _ = Token.objects.get_or_create(user=user)
        if token:
            login(self.request, form.get_user())
        return super(Login, self).form_valid(form)


class event_list(APIView, TemplateView):
    renderer_classes = (TemplateHTMLRenderer,)
    permission_classes = (IsAuthenticated,)
    renderer_classes = (TemplateHTMLRenderer,)
    template_name = 'Event_List.html'

    def get(self, request):
        user = request.user.id
        events = create_event.objects.filter(user_id=user)
        serializer = serializers.EventSerializer(events, many=True)
        return Response(serializer.data, template_name='Hoja2.html')

    def post(self, request):
        serializer = serializers.EventoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED, template_name='Hoja2.html')
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST, template_name='Hoja3.html')


class event_detail(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, event_id):
        try:
            user = request.user.id
            # event = request.event.id
            eventos = create_event.objects.filter(user_id=user, pk=event_id)
        except create_event.DoesNotExist:
            raise Http404
        serializer = serializers.EventSerializer(eventos)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, event_id):
        try:
            user = request.user.id
            eventos = create_event.objects.get(owner=user_id, pk=event_id)
        except create_event.DoesNotExist:
            raise Http404
        serializer = serializers.EventSerializer(eventos, data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, event_id):
        try:
            user_id = request.user
            eventos = create_event.objects.get(owner=user_id, pk=event_id)
        except create_event.DoesNotExist:
            raise Http404
        serializer = serializers.EventSerializer(eventos)
        res = serializer.data
        eventos.delete()
        return Response(status=status.HTTP_200_OK)


@csrf_exempt
def create_event_f(request):
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)
    usr = request.user
    formularioIns = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST)
        event = create_event(event_name=form['event_name'].value(),
                             event_category=form['event_category'].value(),
                             event_place=form['event_place'].value(),
                             event_address=form['event_address'].value(),
                             event_initial_date=form['event_initial_date'].value(),
                             event_final_date=form['event_final_date'].value(),
                             event_type=form['event_type'].value(),
                             thumbnail=form['thumbnail'].value(),
                             user_id=usr)
        event.save()
        return render(request, 'registro2.html', {'form': formularioIns})
    else:
        formularioIns = EventForm()
    return render(request, 'InsEvento.html', {'form': formularioIns})

@csrf_exempt
def events_list(request):
    user = request.user.id
    queryset = create_event.objects.filter(user_id=user)
    serializer_class = EventSerializer
    permission_classes = (IsAuthenticated,)
    authentication_class = (TokenAuthentication,)
    return render(request, 'Event_List.html', {'queryset': queryset})


def delete_event(request, event_id):
    user = request.user.id
    queryset = create_event.objects.filter(user_id=user)
    try:
        event = create_event.objects.get(id=event_id)
    except create_event.DoesNotExist:
        raise Http404
    event.delete()
    return redirect('http://172.24.98.163:8080/api/events/list/')


@csrf_exempt
def update_event(request, event_id):
    user = request.user.id
    event = create_event.objects.get(user_id=user, pk=event_id)
    form = EventForm(request.POST, instance=event)
    print('Entrar al formulario')
    if form.is_valid():
        print('Entré al formulario')
        form.save()
        return redirect("http://172.24.98.163:8080/api/eventos/")
    return render(request, 'Hoja4.html', {'event': event, 'form':form})

def logout(request):
    do_logout(request)
    return redirect('http://172.24.98.163:8080/login/')