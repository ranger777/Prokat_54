function validateImage() {
  var fileInput = document.getElementById('photo');
  var filePath = fileInput.value;
    if (!filePath == ''){

  var allowedExtensions = /(\.jpg|\.jpeg|\.png|\.gif)$/i;
  if (!allowedExtensions.exec(filePath)) {
    alert('Не верный тип файла, выберите JPG, JPEG, PNG или GIF изображение');
    fileInput.value = '';
    return false;
  } else if (fileInput.files[0].size > 5 * 1024 * 1024) {
    alert('Файл превышает допустимые 5 MB');
    fileInput.value = '';
    return false;
  } else {
    return true;
  }
    }

}