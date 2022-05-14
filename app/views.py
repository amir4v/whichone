from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import AVote, Option, Rather
from django.db.models import Q
import random


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(request):
    return render(request, 'home.html')


def votes(request):
    votes = AVote.objects.all()
    return render(request, 'votes.html', {'votes':votes})


def avote(request, id):
    ip = get_client_ip(request)
    avote = AVote.objects.get(id=id)

    ##########
    options = avote.option_set.values('id').all()
    options_number = options.count()
    options_number = options_number*(options_number-1) //2

    ip_choosed = avote.rather_set.values('choosed', 'refused').filter(ip=ip)
    ip_choosed_number = ip_choosed.count()

    if(ip_choosed_number >= options_number):
        return render(request, 'avote.html', {'mesh':True, 'avote': id})
    
    while(True):
        a = random.choice(options)
        b = random.choice(options)
        if a==b:
            continue
        flag = ( {'choosed': a.get('id'), 'refused': b.get('id')} not in ip_choosed ) \
                and \
                ( {'choosed': b.get('id'), 'refused': a.get('id')} not in ip_choosed )
        if(flag):
            a = a.get('id')
            b = b.get('id')
            break
    
    ab = Option.objects.filter(avote=avote).filter( Q(id=a) | Q(id=b) )
    if ab.count() != 2:
        return HttpResponse(str(ab.count()))
    return render(request, 'avote.html', {
        'A': ab[0],
        'B': ab[1],
        'avote': id,
    })
    ##########

    # Down
    # options = avote.option_set.all()
    # options_number = options.count()
    # options_number = options_number*(options_number-1) //2

    # ip_choosed = avote.rather_set.filter(ip=ip)
    # ip_choosed_number = ip_choosed.count()

    # if(ip_choosed_number >= options_number):
    #     return render(request, 'avote.html', {'mesh':True, 'avote': id})


    # makeit_for_options = []
    # for o in options:
    #     for oo in options:
    #         if (o==oo) or ([o,oo] in makeit_for_options) or ([oo,o] in makeit_for_options):
    #             continue
    #         makeit_for_options.append([o, oo])
    
    # ip_choosed
    # for c in ip_choosed:
    #     for m in makeit_for_options:
    #         if (c.l() == m) or (c.lr() == m):
    #             makeit_for_options.remove(m)


    # return render(request, 'avote.html', {
    #     'A': makeit_for_options[0][0],
    #     'B': makeit_for_options[0][1],
    #     'avote': id,
    # })
    # Down


def avote_result(request, id):
    avote = AVote.objects.get(id=id)
    result = avote.option_set.order_by('-score')[:10]

    return render(request, 'avote-result.html', {'result':result, 'avote':avote})


def rather(request, avote, choosed, refused):
    ip = get_client_ip(request)
    avote = AVote.objects.get(id=avote)

    # CHECK
    zero = Rather.objects.filter(ip=ip, avote=avote) \
                    .filter(
                            Q(choosed__id=choosed, refused__id=refused) | Q(choosed__id=refused, refused__id=choosed)
                            ).count()
    if zero!=0:
        return redirect('/avote/'+ str(avote.id))

    r = Rather()
    r.ip = ip
    r.avote = avote
    r.choosed = Option.objects.get(id=choosed) # TODO Behine shavad
    r.refused = Option.objects.get(id=refused) # TODO Behine shavad
    r.save()

    option = Option.objects.get(id=choosed) # TODO Behine shavad
    option.score += 1
    option.save()

    return redirect('/avote/'+ str(avote.id))