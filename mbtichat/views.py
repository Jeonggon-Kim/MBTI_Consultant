from django.shortcuts import render, redirect
import openai, os 
from openai import OpenAI
from dotenv import load_dotenv
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import *
load_dotenv()

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
  user = request.user
  if not user.is_authenticated or user.is_staff:
    return redirect('/login')  
  
  api_key = os.getenv("OPENAI_KEY", None)
  client = OpenAI(api_key=api_key)
  openai.api_key = api_key
  chatbot_response = None
  chats = Chat.objects.filter(user=user)

  if api_key is not None and request.method == 'POST' :
    prompt = request.POST.get('user_input') 
    messages = []
    messages.append({"role" : "assistant", "content" : '안녕하세요. 저는 MBTI 상담가입니다. 당신의 고민을 당신의 mbti와 관련해서 해결해드립니다! MBTI가 어떻게 되시나요?'})
    messages.append({"role": "system", "content": "Your job is to consult the user regarding his or her mbti. When the user tells you the mbti, you have to ask what kind of problem that he has that he wants to consult with you. every response that you give should be related to mbti"})      
    messages.append({"role": "system", "content": "When the person says his mbti is ESFJ, you tell him that statistically, most unlikable mbti is esfj."})      
    for chat in chats :
      messages.append({"role" : "user", "content" : chat.prompt})
      messages.append({"role" : "assistant", "content" : chat.response})
    messages.append({"role" : "user", "content" : prompt})
    
    response = client.chat.completions.create(
      model = 'gpt-3.5-turbo',
      messages= messages,
      temperature = 0.5 
    )  

    chatbot_response = response.choices[0].message.content
    Chat.objects.create(user=user,prompt=prompt,response=chatbot_response)
    chats = Chat.objects.filter(user=user)
  return render(request, 'main.html', {'response' : chatbot_response, 'user' : user, "chats": chats})

  