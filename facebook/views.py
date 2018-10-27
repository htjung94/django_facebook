from django.shortcuts import render, redirect
from facebook.models import Article, Comment

# Create your views here.

def play(request) :
    return render(request, 'play.html')

count = 0
def play2(request) :
    junghyuntae = '정현태'
    age = 20

    global count
    count = count + 1

    if age > 19 :
        status = '성인'
    else :
        status = '청소년'

    diary = ['오늘은 날씨가 맑았따. - 4월 3일', '미세먼지가 너무 심하다. (4월 2일)', '비가 온다. 4월 1일에 작성']

    return render(request, 'play2.html', {'name' : junghyuntae, 'cnt' : count, 'age' : status, 'diary' : diary})


def profile(request):
    return render(request, 'profile.html')

def event(request):

    junghyuntae = '정현태'
    age = 20

    global count
    count = count + 1

    if age > 19:
        status = '성인'
    else:
        status = '청소년'

    if count == 7:
        lotto = '당첨!'
    else:
        lotto = '꽝...'
    return render(request, 'event.html', {'name' : junghyuntae, 'cnt' : count, 'age' : status , 'lotto' : lotto})

def newsfeed(request):
    # 여기서 DB에서 글을 불러와서 newsfeed.html로 보내주자

    articles = Article.objects.all()
    return render(request, 'newsfeed.html', { 'articles' : articles })

def detail_feed(request, pk):
    #pk번 글을 불러오기
    article = Article.objects.get(pk = pk)

    #comment data를 받아서 등록
    if request.method == 'POST' :
        Comment.objects.create(
            article =article,
            author=request.POST['nickname'],
            text=request.POST['reply'],
            password=request.POST['password']
        )
    return render(request, 'detail_feed.html', { 'feed' : article })

def new_feed(request) :
    #데이터베이스 저장하는 작업하는 함수

    # 사용자가 게시버튼을 눌렀는지를 확인해야함
    if request.method == 'POST' :
        #글 저장
        new_article = Article.objects.create(
            author = request.POST['author'],
            title = request.POST['title'],
            text = request.POST['content'],
            password = request.POST['password']
        )

    return render(request, 'new_feed.html')

def edit_feed(request, pk) :
    article = Article.objects.get(pk = pk)

    # 실제로 수정한 내용을 저장
    if request.method == 'POST' : # 수정버튼을 눌렀다.
        if request.POST['password'] == article.password:
            article.title = request.POST['title']
            article.author = request.POST['author']
            article.text = request.POST['content']
            article.save()
            return redirect(f'/feed/{ pk }')
    # return redirect('/feed/' + str(pk))
    # return redirect(f'/feed/{ article.pk }')

    return render(request, 'edit_feed.html', { 'feed' : article })

def remove_feed(request, pk) :
    article = Article.objects.get(pk=pk)

    #삭제 로직
    if request.method == 'POST' :
        # request.POST['password'] -> 사용자가 입력한 비밀벊
        # 진짜 비밀번호 : article.password에 저장되어있음
        if request.POST['password'] == article.password:
            article.delete()
            return redirect('/')
    return render(request, 'remove_feed.html',{ 'feed' : article })