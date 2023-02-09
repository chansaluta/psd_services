from django.db import models

import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
# Create your models here.


class outpass_locator_staff_details(models.Model):
    auth_user_id = models.IntegerField()
    id_number = models.CharField(max_length=16)
    first_name = models.CharField(max_length=64)
    middle_name = models.CharField(max_length=32)
    last_name = models.CharField(max_length=32)
    ext_name = models.CharField(max_length=16)
    full_name = models.CharField(max_length=128,null=True)
    position = models.CharField(max_length=32)
    status = models.IntegerField()
    program = models.CharField(max_length=64, null=True)
    qr_code = models.ImageField(upload_to='outpass_locator/staff_qr_code', blank=True)
    image = models.ImageField(upload_to='outpass_locator/staff_image', null=True)
    current_official_outpass_id = models.IntegerField(null=True)
    current_personal_outpass_id = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    outpass_locator_program_id = models.IntegerField(null=True)

    def save(self, *args, **kwargs):
        qr_code_image = qrcode.make(self.id_number)
        canvas = Image.new('RGB',(290, 290), 'white')
        canvas.paste(qr_code_image)
        qr_id_number = f'qr_code-{self.id_number}.png'
        buffer = BytesIO()
        canvas.save(buffer,'PNG')
        self.qr_code.save(qr_id_number,File(buffer),save=False)
        canvas.close()
        super().save(*args,**kwargs)
    
    def get_firstname_title(self):
        return self.first_name.title()

    def get_lastname_title(self):
        return self.last_name.title()
    
    def get_middlename_title(self):
        return self.middle_name.title() if self.middle_name else ""
    
    @property
    def get_fullname(self):
        if self.first_name:
            return "{} {}. {}".format(self.first_name.title(), self.middle_name[:1], self.last_name.title()) if self.middle_name else "{} {}".format(self.first_name.title(), self.last_name.title())
        else:
            return None
    
    def get_status(self):
        if self.status == 1:
            return "Office"
        elif self.status == 2:
            return "Outpass"
        elif self.status == 3:
            return "Outpass Approved"
        elif self.status == 4:
            return "RSO"
        elif self.status == 5:
            return "Travel"
        elif self.status == 6:
            return "On Leave"
    
    def get_color(self):
        if self.status == 1:
            return "primary"
        elif self.status == 2:
            return "info"
        elif self.status == 3:
            return "success"
        elif self.status == 4:
            return "danger"
        elif self.status == 5:
            return "danger"
        elif self.status == 6:
            return "danger"
    
    def get_icon(self):
        if self.status == 1:
            return "fa-desktop"
        elif self.status == 2:
            return "fa-check-square"
        elif self.status == 3:
            return "fa-clock-o"
        elif self.status == 4:
            return "fa-suitcase"
        elif self.status == 5:
            return "fa-plane"
        elif self.status == 6:
            return "fa-share-square-o"
    

    class Meta:
        db_table = "outpass_locator_staff_details"


class outpass_locator_logs(models.Model):
    id_number = models.CharField(max_length=16)
    user_id = models.IntegerField()
    outpass_locator_staff_details_id = models.IntegerField()
    inclusive_dates = models.TextField()
    time_check_out = models.CharField(max_length=16)
    time_check_in = models.CharField(max_length=16)
    time_span_outpass = models.CharField(max_length=16)
    month = models.CharField(max_length=12,null=True)
    if_approved = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "outpass_locator_logs"


class official_outpass_locator_logs(models.Model):
    id_number = models.CharField(max_length=16)
    user_id = models.IntegerField()
    outpass_locator_staff_details_id = models.IntegerField()
    inclusive_dates = models.TextField()
    time_check_out = models.CharField(max_length=16)
    time_check_in = models.CharField(max_length=16)
    time_span_outpass = models.CharField(max_length=16)
    month = models.CharField(max_length=12,null=True)
    remarks = models.TextField(null=True)
    place_visited = models.TextField(null=True)
    if_approved = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = "official_outpass_locator_logs"





class outpass_locator_program(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=32)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "outpass_locator_program"