from django.db import models

class Note(models.Model): 
  title = models.CharField(max_length=100)
  content = models.TextField()
  created_at = models.DateTimeField(auto_now_add= True)

  def __str__(self):
    return self.title
  
class NoteImage(models.Model):
  note = models.ForeignKey(Note, on_delete=models.CASCADE, related_name='images')
  image = models.ImageField(upload_to='images/')
  
  def __str__(self):
    return f"Image for {self.note.title}"