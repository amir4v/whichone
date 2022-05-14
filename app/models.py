from django.db import models


class AVote(models.Model):
    title = models.CharField(max_length=200)


    def __str__(self):
        return self.title


class Option(models.Model):
    avote = models.ForeignKey(AVote, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    score = models.IntegerField(default=0)


    def __str__(self):
        return self.title


class Rather(models.Model):
    ip = models.CharField(max_length=50)

    avote = models.ForeignKey(AVote, on_delete=models.CASCADE)
    choosed = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='choosed')
    refused = models.ForeignKey(Option, on_delete=models.CASCADE, related_name='refused')


    def __str__(self):
        return str(self.choosed) + ' > ' + str(self.refused)
    

    def l(self):
        return [self.choosed, self.refused]
    
    def lr(self):
        return [self.refused, self.choosed]