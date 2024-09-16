import app

if __name__ == "__main__":
    
    myApp = app.App(640, 480, 'Vulkan application', True)

    myApp.run()
    
    myApp.close()