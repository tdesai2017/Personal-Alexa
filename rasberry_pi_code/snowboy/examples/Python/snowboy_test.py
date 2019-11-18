import snowboydecoder
def detected_callback():
    print ("hotword detected")
detector = snowboydecoder.HotwordDetector("Alexa.pmdl", sensitivity=0.4, audio_gain=1)
detector.start(detected_callback)