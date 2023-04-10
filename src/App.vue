<template>
  <div class="app main" @click="toggleMic">
    <div>
      <div class="title">PULSA EN LA PANTALLA PARA PREGUNTAR</div>

      <div>
        <div v-if="!isRecording" class="transcript">{{ capitalizeFirstLetter(question) }}</div>
      </div>

      <div>
        <div v-if="isAnswerReady" class="transcript">{{ answer }}</div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

const question = ref<string>('')
const answer = ref<string>('')
const isRecording = ref<boolean>(false)
const isAnswerReady = ref<boolean>(false)
const backgoundColor = ref<string>('#281936')

// @ts-ignore
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition
const sr = new Recognition()

onMounted(() => {
  sr.continuous = true
  sr.interimResults = true
  sr.lang = 'es-ES'
})

const toggleMic = () => {
  if (isRecording.value) {
    sr.stop()
  } else {
    sr.start()
    question.value = ''
    answer.value = ''
  }
}

sr.onstart = () => {
  isRecording.value = true
  backgoundColor.value = '#0f451f'
}

sr.onend = () => {
  isRecording.value = false
  isAnswerReady.value = false
  backgoundColor.value = '#281936'
  sendQuestion(question.value)
}

// @ts-ignore
sr.onresult = (event) => {
  question.value = event.results[event.results.length - 1][0].transcript
}

const url = 'https://api.openai.com/v1/chat/completions'

const headers = {
  'Content-Type': 'application/json',
  Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`
}

const sendQuestion = (question: String) => {
  console.log(question)

  if (question === '') return

  fetch(url, {
    method: 'POST',
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: [{ role: 'user', content: question }],
      temperature: 0.2
    }),
    headers: headers
  })
    .then((response) => response.json())
    .then((data) => {
      isAnswerReady.value = true
      answer.value = data.choices[0].message.content
      speak(answer.value)
    })
    .catch((error) => console.error('Error:', error))
}

const synth = window.speechSynthesis

const speak = (text: string) => {
  if (synth.speaking) {
    console.error('speechSynthesis.speaking')
    return
  }

  const utterThis = new SpeechSynthesisUtterance(text)

  utterThis.onend = function (event) {
    console.log('SpeechSynthesisUtterance.onend')
  }

  utterThis.onerror = function (event) {
    console.error('SpeechSynthesisUtterance.onerror')
  }

  const selectedOption = 'Sandy (Spanish (Spain))'
  const voices = synth.getVoices()

  for (let i = 0; i < voices.length; i++) {
    if (voices[i].name === selectedOption) {
      utterThis.voice = voices[i]
      break
    }
  }
  utterThis.pitch = 1.1
  utterThis.rate = 0.8
  utterThis.lang = 'es-ES'

  synth.speak(utterThis)
}

function capitalizeFirstLetter(string: string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Fira sans', sans-serif;
}

.main {
  min-height: 100vh;
  background-color: v-bind(backgoundColor);
}

.title {
  display: flex;
  justify-content: center;
  padding-top: 10%;
  color: white;
}

.transcript {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 75%;
  margin: 5% auto;
  font-size: 30px;
  color: white;
}
</style>
