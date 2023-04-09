<template>
  <div class="app main" @click="toggleMic">
    <div class="mic-status">Está el micro escuchando? {{ isRecording ? 'Si' : 'No' }}</div>
    <div>
      <div class="transcript">{{ transcript }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const transcript = ref<String>('')
const isRecording = ref<Boolean>(false)
const backgoundColor = ref<String>('#281936')

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
  }
}

sr.onstart = () => {
  console.log('Grabando')
  isRecording.value = true
  backgoundColor.value = '#0f451f'
}

sr.onend = () => {
  console.log('SR Stopped')
  isRecording.value = false
  backgoundColor.value = '#281936'
}

sr.onresult = (event) => {
  console.log(event.results)

  for (let i = 0; i < event.results.length; i++) {
    const result = event.results[i]
    if (result.isFinal) checkQuestion(result)
  }

  const t = Array.from(event.results)
    .map((result) => result[0])
    .map((result) => result.transcript)
    .join('')

  transcript.value = t
}

const checkQuestion = (result) => {
  const t = result[0].transcript
  if (t.includes('final del audio')) {
    sr.stop()
  }
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
  min-width: 100vh;
  background-color: v-bind(backgoundColor);
}

.mic-status {
  color: white;
  display: flex;
  justify-content: center;
  padding-top: 5%;
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
