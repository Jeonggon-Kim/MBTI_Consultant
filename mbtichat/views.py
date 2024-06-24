from django.shortcuts import render, redirect
import openai, os 
from openai import OpenAI
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *

def user_logout(request):
  if request.method == 'POST' :
   logout(request)
  return redirect('/')

def sign_up(request):
  if request.method == 'POST' : 
    username = request.POST.get('username')
    password = request.POST.get('password')
    User.objects.create_user(username,None,password)
    return redirect('/login')
  else : 
    return render(request, 'sign_up.html')

def user_login(request):
  if request.method == 'POST':
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      return redirect('/')  
    else:
      return render(request, 'login.html', {'error': 'Invalid username or password'})
  else:
    return render(request, 'login.html')


def main_page(request):
  print('1')
  user = request.user
  if not user.is_authenticated or user.is_staff:
    return redirect('/login')    
  else:
    load_dotenv()
    api_key = os.getenv("OPENAI_KEY", None)
    chats = Chat.objects.filter(user=user)

    client = OpenAI(api_key=api_key)
    chatbot_response = None
    if api_key is not None and request.method == 'POST' :
      print('2')
      openai.api_key = api_key
      user_input = request.POST.get('user_input')
      print('3')
      prompt = user_input 
      messages = []
      messages.append({"role" : "assistant", "content" : '안녕하세요. mbti가 어떻게 되시나요?'})
      messages.append({"role": "system", "content": "Your job is to consult the user regarding his or her mbti. When the user tells you the mbti, you have to ask what kind of problem that he has that he wants to consult with you. every response that you give should be related to mbti"})      
      print('4')

      for chat in chats :
        messages.append({"role" : "user", "content" : chat.prompt})
        messages.append({"role" : "assistant", "content" : chat.response})
      messages.append({"role" : "user", "content" : prompt})
      print('4.5')
      print(messages)
      response = client.chat.completions.create(
        model = 'gpt-3.5-turbo',
        messages= messages,
        temperature = 0.5 
      )  
      print('5')

      chatbot_response = response.choices[0].message.content
      Chat.objects.create(user=user,prompt=prompt,response=chatbot_response)
      chats = Chat.objects.filter(user=user)
      print('6')
  return render(request, 'main.html', {'response' : chatbot_response, 'user' : user, "chats": chats})
