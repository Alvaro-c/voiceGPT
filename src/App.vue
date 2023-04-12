<template>
  <div class="app main" @click="toggleMic">
    <div class="conversation">
      <div class="title">PULSA EN LA PANTALLA PARA PREGUNTAR</div>

      <div v-for="message in conversation" :key="message.content">
        <div class="role">{{ message.role === 'user' ? 'Pregunta' : 'Respuesta' }}</div>
        <div class="transcript">{{ capitalizeFirstLetter(message.content) }}</div>
      </div>

      <div v-if="conversation.length > 0" ref="endOfConversation" class="endOfConversation">
        PULSA LA PANTALLA PARA SEGUIR PREGUNTANDO
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface Message {
  role: string
  content: string
}

const isMicPermited = ref<boolean>(false)
const question = ref<string>('')
const answer = ref<string>('')
const isRecording = ref<boolean>(false)
const isAnswerReady = ref<boolean>(false)
const backgoundColor = ref<string>('#281936')
const conversation = ref<Message[]>([])
const endOfConversation = ref(null)
const canVibrate = window.navigator.vibrate

// @ts-ignore
const Recognition = window.SpeechRecognition || window.webkitSpeechRecognition
const sr = new Recognition()

onMounted(() => {
  sr.continuous = true
  sr.interimResults = true
  sr.lang = 'es-ES'
})

const toggleMic = () => {
  if (!isMicPermited.value) {
    speak('')
    // @ts-ignore
    if (canVibrate) navigator.vibrate(200)
    console.log('Mic and vibration are now allowed.')
    isMicPermited.value = true
    toggleMic()
  }

  if (synth.speaking) {
    synth.cancel()
    return
  }

  if (isRecording.value) {
    sr.stop()
  } else {
    sr.start()
    // @ts-ignore
    if (canVibrate) navigator.vibrate(200)
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
  // @ts-ignore
  if (canVibrate) navigator.vibrate([200, 200, 200])

  if (question.value === '') return

  conversation.value.push({
    role: 'user',
    content: question.value
  })
  sendQuestion()
  scroll()
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

const sendQuestion = () => {
  fetch(url, {
    method: 'POST',
    body: JSON.stringify({
      model: 'gpt-3.5-turbo',
      messages: conversation.value,
      temperature: 0.2
    }),
    headers: headers
  })
    .then((response) => response.json())
    .then((data) => {
      isAnswerReady.value = true
      answer.value = data.choices[0].message.content
      speak(answer.value)
      conversation.value.push(data.choices[0].message)
      scroll()
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
    scroll()
  }

  utterThis.onerror = function (event) {}

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

const scroll = () => {
  // @ts-ignore
  endOfConversation.value.scrollIntoView({ behaviour: 'smooth' })
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

.conversation {
  overflow-x: hidden;
  overflow-y: visible;
}

.role {
  font-size: 30px;
  font-weight: bold;
  text-decoration: underline;
  color: white;
}

.transcript {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 85%;
  margin: 5% auto;
  font-size: 30px;
  color: white;
}

.endOfConversation {
  color: white;
  margin: 10% auto;
  display: flex;
  justify-content: center;
  align-items: center;
}
</style>
