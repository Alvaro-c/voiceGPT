<template>
  <div class="app main">
    <div class="mic-status">Está el micro grabando? {{ isRecording ? 'Si' : 'No' }}</div>
    <button class="center m-top-5 record-button" @click="toggleMic">RECORD</button>
    <button class="center m-top-5 record-button" @click="test">TEST</button>

    <div>
      <div v-if="!isRecording" class="transcript">{{ speechResult }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
const speechResult = ref<String>('')
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
  isRecording.value = true
  backgoundColor.value = '#0f451f'
}

sr.onend = () => {
  isRecording.value = false
  backgoundColor.value = '#281936'
}

sr.onresult = (event) => {
  speechResult.value = event.results[event.results.length - 1][0].transcript
}

const test = () => {
  console.log('test')
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

.center {
  display: flex;
  justify-content: center;
  margin: auto;
}

.m-top-5 {
  margin-top: 5%;
}

.record-button {
  width: 140px;
  height: 50px;
  display: flex;
  justify-content: center;
  align-items: center;
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
