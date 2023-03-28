<h1 align="center"> VkClient </h1>

<p align="center">
  Client for vk.com using RSA encryption.
</p>

<p align="center">
  <img src="https://github.com/1Danieru/VkClient/blob/main/screenshots/main.png"/>
</p>


# How to use the client
To use the client you need to get **USER ID** and **TOKEN**. After receiving the data, click **Connect**. The second user must do the same.

  ## _How to get a TOKEN_
  To get a token, click **Get TOKEN**.
  
  1. Click **Allow**.
  2. Copy the part of the address bar from **access_token=** to **&expires_in**.
  
  ## _How to get a USER'S ID_
  To get a **USER ID**, go to the page of the user with whom you want to start a dialogue and copy his id from the address bar.
    
  **Example:** _https://vk.com/123456789_
  
  _You need to take only '123456789'_
  
  ### _Note_
  User's ID must be in the form of numbers. If the user has a custom ID, then you need to get a real (digital) one.
  
  > The VK ID is an identifier of a user or community. The user profile URL looks like https://vk.com/idXXXXXX, where XXXXXX is the profile ID. You can see the ID in your browser’s address bar. If the profile or has an alphanumeric short name, the ID can be found as such: open any photo of a user and check the URL: the first numbers after the word “photo” (XXXXXX in a URL like https://vk.com/photoXXXXXX_YYYYYYY) is the ID you’re looking for.

  ## _How to delete unnecessary files_
  After using the client, the folder will contain .bin .db .pem files. To quickly remove them, click **Clean**.


  ## _Mandatory conditions_
  - Make sure that the dialogue with the user has already begun.
  - Make sure both you and the user have private messages open.

# PY TO EXE
Make sure you have [Python 3.7+](https://www.python.org/downloads/)

_to-requirements.txt allows to automatically add modules to requirements.txt installing them using pip._
```
  pip install to-requirements.txt
```

_Create a .exe on Windows with pyinstaller._
```
  pyinstaller --noconfirm --onedir -F --windowed --add-data "<CustomTkinter Location>/customtkinter;customtkinter/"  "<Path to Python Script>"
```

# License
GPLv3, see [LICENSE](https://github.com/1Danieru/VkClient/blob/main/LICENSE) for additional info.
