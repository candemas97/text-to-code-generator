<template>
    <div>
        <button @click="startRecording('english')">Start Recording in English</button>
        <button @click="startRecording('spanish')">Comenzar Grabación en Español</button>
        <button @click="stopRecording" :disabled="!isRecording">Stop Recording</button>
    </div>
</template>

<script lang="ts">
import { defineComponent } from "vue";
declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

type Language = "english" | "spanish";

export default defineComponent({
    data(): {
        isRecording: boolean;
        mediaRecorder: MediaRecorder | null;
        recognition: any;
    } {
        return {
            isRecording: false,
            mediaRecorder: null,
            recognition: null,
        };
    },
    methods: {
        setupSpeechRecognition(language: Language) {
            const languageMap: Record<Language, string> = {
                english: "en-US",
                spanish: "es-ES",
            };

            const SpeechRecognition: any = window.SpeechRecognition || window.webkitSpeechRecognition;
            if (SpeechRecognition) {
                this.recognition = new SpeechRecognition();
                this.recognition.lang = languageMap[language];
                this.recognition.interimResults = false;
                this.recognition.maxAlternatives = 1;
                this.recognition.onresult = (event: any) => {
                    const transcript = event.results[0][0].transcript;
                    console.log("Recognized Text:", transcript);
                };
            } else {
                console.error("Speech recognition API is not supported in this browser.");
            }
        },
        async startRecording(language: Language) {
            if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                try {
                    const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
                    this.mediaRecorder = new MediaRecorder(stream);
                    this.mediaRecorder.start();
                    this.isRecording = true;
                    this.setupSpeechRecognition(language);
                    this.recognition?.start();
                } catch (err) {
                    console.error("Error starting recording:", err);
                }
            } else {
                console.error("getUserMedia not supported in this browser");
            }
        },
        stopRecording() {
            if (this.mediaRecorder) {
                this.mediaRecorder.stop();
                this.recognition?.stop();
                this.isRecording = false;
            }
        },
    },
});
</script>

<style>
/* Add styles here if necessary */
</style>
