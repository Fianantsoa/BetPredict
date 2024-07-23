[app]
# Use the Kivy language (python)
language = python2

# Use the SDL2 graphics library
graphics = sdl2

# Use the Android platform
platform = android

# Use the default Android SDK path
android_sdk = /path/to/android-sdk

# Use the default Android NDK path
android_ndk = /path/to/android-ndk

# Use the default Android deploy key
android_deploy_key = /path/to/android-deploy-key

# Use the default Android build tools
android_build_tools = /path/to/android-build-tools

# Use the default Android platform version
android_api_level = 28  # Change this to your desired API level

# Use the default Android minimum API level
android_min_api_level = 21  # Change this to your minimum supported API level

# Use the default Android target SDK version
android_target_sdk_version = 28  # Change this to your target SDK version

# Use the default Android target architecture
android_target_arch = armeabi-v7a  # Change this to your desired architecture

# Use the default Android screen orientation
android_orientation = sensor        #portrait en cas contraire

# Use the default Android window size
android_window_size = 800x480  # Change this to your desired window size

# **Add the missing information**
title = PreditBet  # Replace with your desired app title
source.dir = .
package.name = com.PreditBet.myapp  # Replace with your desired package name (unique identifier)
package.domain = org.yourdomainPreditBet
source.include_exts = py,png,jpg,kv,atlas
version = 0.1  # Set the application version

android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Use the default Android statusbar icon
android_statusbar_icon = @myapp/icon.png  # Replace with your icon path

# Use the default Android splash screen icon
android_icon = @myapp/icon.png  # Replace with your icon path

[build]
# Use the default Kivy build tools
log_level = 2

# Use the default Kivy build directory
build_dir = ./android

android.add_javac_options = -source 1.8 -target 1.8
