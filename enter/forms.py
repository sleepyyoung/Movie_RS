from django import forms
from captcha.fields import CaptchaField


class RegisterForm(forms.Form):
    nickname = forms.CharField(
        required=True,
        label="请输入昵称:",
        max_length=11,
        error_messages={"invalid": "昵称最长只能输入11位！"}
    )
    username = forms.EmailField(
        required=True,
        label="请输入邮箱(用户名):",
    )
    first_password = forms.CharField(
        required=True,
        min_length=8,
        label="请输入密码:",
        widget=forms.PasswordInput(),
    )
    second_password = forms.CharField(
        required=True,
        label="请确认密码:",
        widget=forms.PasswordInput(),
    )
    captcha = CaptchaField(
        label="请输入验证码结果:",
        required=True,
        error_messages={"invalid": "验证码输入有误,请重新输入"}
    )
    captcha_email = forms.CharField(
        label="请输入邮箱验证码:",
        required=True,
        error_messages={"invalid": "验证码错误"}
    )

    Adventure = forms.CharField(label="冒险(Adventure)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                                required=False, )
    Animation = forms.CharField(label="动画(Animation)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                                required=False, )
    Children = forms.CharField(label="儿童(Children)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                               required=False, )
    Comedy = forms.CharField(label="喜剧(Comedy)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                             required=False, )
    Fantasy = forms.CharField(label="幻想(Fantasy)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                              required=False, )
    Romance = forms.CharField(label="爱情(Romance)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                              required=False, )
    Action = forms.CharField(label="动作(Action)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                             required=False, )
    Crime = forms.CharField(label="犯罪(Crime)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                            required=False, )
    Thriller = forms.CharField(label="惊悚(Thriller)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                               required=False, )
    Horror = forms.CharField(label="恐怖(Horror)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                             required=False, )
    FilmNoir = forms.CharField(label="暗黑(Film-Noir)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                               required=False, )
    Drama = forms.CharField(label="戏剧(Drama)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                            required=False, )
    Mystery = forms.CharField(label="神秘(Mystery)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                              required=False, )
    SciFi = forms.CharField(label="科幻(Sci-Fi)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                            required=False, )
    War = forms.CharField(label="战争(War)", widget=forms.TextInput(attrs={'style': 'display:none'}), required=False, )
    Western = forms.CharField(label="西部(Western)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                              required=False, )
    Musical = forms.CharField(label="音乐(Musical)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                              required=False, )
    IMAX = forms.CharField(label="IMAX(IMAX)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                           required=False, )
    Others = forms.CharField(label="其它(Others)", widget=forms.TextInput(attrs={'style': 'display:none'}),
                             required=False, )

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class LoginForm(forms.Form):
    user = forms.CharField(
        required=True,
        label="请输入账号(邮箱):",
        widget=forms.TextInput(attrs={'placeholder': '账号'}),
    )
    password = forms.CharField(
        required=True,
        label="请输入密码:",
        widget=forms.PasswordInput(attrs={'placeholder': '密码'}),
    )
    captcha = CaptchaField(
        label="请输入验证码结果:",
        required=True,
        error_messages={"invalid": "验证码输入有误,请重新输入"}
    )

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })


class ForgotPasswordForm(forms.Form):
    username = forms.EmailField(
        required=True,
        label="用户名(邮箱):",
    )
    captcha_email = forms.CharField(
        label="请输入邮箱验证码:",
        required=True,
        error_messages={"invalid": "验证码错误"}
    )
    first_password = forms.CharField(
        required=True,
        min_length=8,
        label="请输入密码:",
        widget=forms.PasswordInput(),
    )
    second_password = forms.CharField(
        required=True,
        label="请确认密码:",
        widget=forms.PasswordInput(),
    )

    def __init__(self, *args, **kwargs):
        super(ForgotPasswordForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
            })
