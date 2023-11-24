from django import forms
from .models import CustomUser, Post, Rating

class CustomUserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        if password != password2:
            raise forms.ValidationError("Passwords do not match.")

    def save(self, commit=True):
        user = super(CustomUserRegistrationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])  # Securely hash the password
        if commit:
            user.save()
        return user

class CustomUserLoginForm(forms.Form):
        username = forms.CharField(max_length=150)
        password = forms.CharField(widget=forms.PasswordInput)

class PostForm(forms.ModelForm):
    STATUS_CHOICES = (
       ('lost', 'Lost'),
       ('found', 'Found'),
       ('returned', 'Returned'),
       ('claimed', 'Claimed'),
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Post
        fields = ['description', 'image', 'item_name', 'fo_name', 'time_place', 'status', 'contact']

class EditPostForm(forms.ModelForm):
    STATUS_CHOICES = (
       ('lost', 'Lost'),
       ('found', 'Found'),
       ('returned', 'Returned'),
       ('claimed', 'Claimed'),
    )

    status = forms.ChoiceField(choices=STATUS_CHOICES)

    class Meta:
        model = Post
        fields = ['description', 'image', 'item_name', 'fo_name', 'time_place', 'status', 'contact']

class EditProfileForm(forms.ModelForm):
    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
    )
    
    gender = forms.ChoiceField(choices=GENDER_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['full_name', 'gender', 'email', 'address', 'contact', 'profile_pic']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['ratings', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3}),
            'ratings': forms.TextInput(attrs={'type': 'number', 'min': 1, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = False
        
        ratings = forms.IntegerField(
        label='Ratings',
        widget=forms.TextInput(attrs={'type': 'number', 'min': 1, 'max': 5})
    )
   
class SearchForm(forms.Form):
    search_query = forms.CharField(max_length=100, label='Search')
