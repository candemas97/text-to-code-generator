<template>
  <section class="container">
    <header>
      <h1 class="titulo">{{ selectedLanguageApp === 'english' ? "The Text-to-Code Generator" : "El Generador Texto a Código"}}</h1>
      <section class="language">
        <span
          :class="{
            'language-label': true,
            'selected-language': selectedLanguageApp === 'english',
          }"
          @click="setSelectedLanguageApp('english')"
        >
          EN
        </span>
        <span class="dot">•</span>
        <span
          :class="{
            'language-label': true,
            'selected-language': selectedLanguageApp === 'spanish',
          }"
          @click="setSelectedLanguageApp('spanish')"
        >
          ES
        </span>
      </section>
    </header>
    <section class="container-2">
      <section class="container-section">
        <textarea
          v-model="query"
          spellcheck="false"
          :placeholder="selectedLanguageApp === 'english' ? 'Write your prompt' : 'Escribe tu prompt'"
        />
        <span class="microphone-container">
          <!-- <MicrophoneIcon class="microphone-icon" @click="ejecutarAlPresionar('ws://localhost:8080/listen-es')" /> -->
          <MicrophoneIcon
            class="microphone-icon"
            @click="startRecording(selectedLanguageApp)"
          />
        </span>
      </section>
      <div class="generating" v-if="isFetching">{{ selectedLanguageApp === 'english' ? "Generating code ..." : "Generando el código ..."}}</div>
      <button @click="requestModel" v-if="!isFetching">{{ selectedLanguageApp === 'english' ? "Execute" : "Ejecutar"}}</button>
      <pre v-if="!isFetching && response.length > 0">
                <code class="language-python">{{ response }}</code>
            </pre>
    </section>
    <!-- <Speech /> -->
    <footer>
      By @yutatys, @sebastianherreramonterrosa, @candemas97
      <span
        ><a href="https://github.com/candemas97/text-to-code-generator" target="_blank"><GithubIcon class="github-icon" /></a
      ></span>
    </footer>
  </section>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import Speech from "./components/Speech.vue";
import MicrophoneIcon from "./assets/MicrophoneIcon.vue";
import hljs from "highlight.js";
import "highlight.js/styles/atom-one-dark.css";
import GithubIcon from "./assets/GithubIcon.vue";

declare global {
  interface Window {
    SpeechRecognition: any;
    webkitSpeechRecognition: any;
  }
}

type Language = "english" | "spanish";

export default defineComponent({
  name: "App",
  components: { MicrophoneIcon, Speech, GithubIcon },
  data: function () {
    return {
      query: "",
      response: "",
      isFetching: false,
      selectedLanguageApp: "english" as Language,
      isRecording: false,
      mediaRecorder: null as MediaRecorder | null,
      recognition: null as any,
    };
  },
  methods: {
    highlightCode(): void {
      this.$nextTick(() => {
        const blocks: NodeListOf<HTMLElement> =
          document.querySelectorAll("pre code");
        blocks.forEach((block: HTMLElement) => {
          hljs.highlightElement(block);
        });
      });
    },
    setSelectedLanguageApp(selectedLanguage: Language) {
      this.selectedLanguageApp = selectedLanguage;
    },
    async requestModel() {
      if (this.query.length > 0) {
        this.isFetching = true;
        const response = await fetch("http://localhost:8080/traslate-to-code", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: this.query,
            idioma: this.selectedLanguageApp,
          }),
        });
        const data = await response.json();
        this.response = data["generateCode"];
        console.log(data);
        this.isFetching = false;
        this.highlightCode();
      }
    },
    setupSpeechRecognition(language: Language) {
      const languageMap: Record<Language, string> = {
        english: "en-US",
        spanish: "es-ES",
      };

      const SpeechRecognition: any =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      if (SpeechRecognition) {
        this.recognition = new SpeechRecognition();
        this.recognition.lang = languageMap[language];
        this.recognition.interimResults = false;
        this.recognition.maxAlternatives = 1;
        this.recognition.onresult = (event: any) => {
          const transcript = event.results[0][0].transcript;
          console.log("Recognized Text:", transcript);
          this.query = transcript;
        };
      } else {
        console.error(
          "Speech recognition API is not supported in this browser."
        );
      }
    },
    async startRecording(language: Language) {
      if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
        try {
          const stream = await navigator.mediaDevices.getUserMedia({
            audio: true,
          });
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
    ejecutarAlPresionar(host_segun_idioma: string) {
      navigator.mediaDevices.getUserMedia({ audio: true }).then((stream) => {
        if (!MediaRecorder.isTypeSupported("audio/webm"))
          return alert("Browser not supported");

        const mediaRecorder = new MediaRecorder(stream, {
          mimeType: "audio/webm",
        });

        const socket = new WebSocket(host_segun_idioma); //ws://localhost:8080/listen-es

        socket.onopen = () => {
          // document.querySelector("#status").textContent = "Connected";
          console.log({ event: "onopen" });
          mediaRecorder.addEventListener("dataavailable", async (event) => {
            if (event.data.size > 0 && socket.readyState == 1) {
              socket.send(event.data);
            }
          });
          mediaRecorder.start(250);
        };

        socket.onmessage = (message) => {
          const received = message.data;
          if (received) {
            console.log(received);
            this.query = received;
          }
        };

        socket.onclose = () => {
          // document.querySelector("#transcript").innerHTML += "<br>";
          console.log({ event: "onclose" });
        };

        socket.onerror = (error) => {
          console.log({ event: "onerror", error });
        };
      });
    },
  },
  mounted() {
    this.highlightCode();
  },
});
</script>

<style scoped lang="scss">
$vp-c-text-1: rgba(255, 255, 245, 0.86);
$vp-c-text-2: rgba(235, 235, 245, 0.6);
$vp-c-text-3: rgba(235, 235, 245, 0.38);

.container {
  width: fit-content;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  margin-top: 3rem;
}

header {
  width: fit-content;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.language {
  display: flex;
  align-items: center;
  margin-inline-end: 1rem;

  & .language-label {
    font-size: 1.4rem;
    font-weight: bolder;
    cursor: pointer;
    color: $vp-c-text-3;
  }

  & .selected-language {
    color: $vp-c-text-2;
    text-decoration: underline;
  }

  & .dot {
    margin: 0 0.3rem 0 0.3rem;
    font-size: 1rem;
  }
}

.container-2 {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  width: 100%;
}
h1 {
  font-size: 72px;
  background: -webkit-linear-gradient(120deg, #bd34fe 50%, #41d1ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  border: none;
  text-align: center;
}

.container-section {
  width: 100%;
  position: relative;
  & textarea {
    margin-top: 1.5rem;
    width: 100%;
    height: 10rem;
    resize: none;
    border: none;
    outline: none;
    background-color: #202127;
    border-radius: 0.8rem;
    padding: 1rem;
    font-size: 1.6rem;
    font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
    color: $vp-c-text-2;

    &::placeholder {
      font-style: italic;
    }
  }

  .microphone-container {
    position: absolute;
    top: 2.5rem;
    right: 1.5rem;
  }

  & .microphone-icon {
    fill: $vp-c-text-2;
    height: 1.6rem;

    &:hover {
      fill: $vp-c-text-3;
      cursor: pointer;
    }
  }
}

.generating {
  margin-top: 1.5rem;
  color: $vp-c-text-2;
  font-size: 1.6rem;
}

button {
  margin-top: 1.5rem;
  width: fit-content;
  font-family: Inter, system-ui, Avenir, Helvetica, Arial, sans-serif;
  font-size: 1.6rem;
  background-color: #646cff;
  color: $vp-c-text-1;
  padding: 0.8rem 1rem;
  text-align: center;
  text-decoration: none;
  display: inline-block;
  font-weight: bolder;
  border: none;
  border-radius: 0.6rem;
  display: flex;
  align-items: center;
  justify-content: center;

  &:hover {
    cursor: pointer;
  }
}

pre {
  margin-top: 1.5rem;
  width: 100%;
  border-radius: 0.8rem;
  font-family: "Cascadia Code", "Fira Code";
  background-color: #202127;
  // height: min-content;
}

code {
  font-family: "Cascadia Code", "Fira Code";
  background-color: #202127;
  font-size: 1.6rem;
}

footer {
  margin-top: 1.5rem;
  color: $vp-c-text-3;
  font-size: 1.4rem;
  display: flex;
  align-items: center;
  justify-content: center;
  & .github-icon {
    fill: $vp-c-text-3;
    height: 1.6rem;
    margin-left: 0.5rem;
    &:hover {
      fill: $vp-c-text-2;
      cursor: pointer;
    }
  }
}
</style>
