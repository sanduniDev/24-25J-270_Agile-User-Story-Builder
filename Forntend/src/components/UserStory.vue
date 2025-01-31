<template>
  <div class="min-h-screen bg-gradient-to-r from-blue-500 to-indigo-600 flex items-center justify-center p-6">
    <div
      class="bg-white rounded-lg shadow-xl p-8 max-w-screen-md w-full transform transition-all duration-500 hover:scale-105">
      <h1 class="text-4xl font-bold text-center text-gray-800 mb-6 animate__animated animate__fadeIn animate__delay-1s">
        User Story Builder</h1>

      <form @submit.prevent="handleSubmit" class="space-y-6">
        <div>
          <label for="audio-file" class="block text-lg font-medium text-gray-800 mb-2">Upload WAV Audio File</label>
          <input type="file" id="audio-file" accept=".wav" @change="handleFileChange"
            class="mt-2 block w-full text-sm text-gray-700 border border-gray-300 rounded-md focus:ring-blue-500 focus:border-blue-500 transition-all duration-300 ease-in-out transform hover:scale-105"
            required />
        </div>

        <button type="submit" :disabled="isSubmitting"
          class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-4 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50 transform transition-all duration-300 ease-in-out hover:scale-105">
          <span v-if="isSubmitting">Processing...</span>
          <span v-else>Submit</span>
        </button>
      </form>

      <div v-if="loading" class="mt-4 text-center text-gray-200 animate__animated animate__fadeIn">Processing your
        request...</div>

      <!-- Error Message -->
      <div v-if="errorMessage"
        class="mt-4 text-center text-red-500 animate__animated animate__fadeIn animate__delay-1s">
        <strong>Error:</strong> {{ errorMessage }}
      </div>

      <!-- Results Section with Beautiful Cards -->
      <div v-if="results.length" class="mt-6 space-y-4">
        <h2 class="text-xl font-medium text-gray-800">Generated Results:</h2>
        <transition-group name="fade" mode="out-in">
          <div class="flex flex-wrap gap-6 w-full">
            <div v-for="(result, index) in results" :key="index"
              class="bg-white rounded-lg shadow-lg p-6 transition-all duration-300 ease-in-out hover:shadow-xl transform hover:scale-105">
              <h3 class="text-lg font-semibold text-gray-800 mb-3">User Story</h3>
              <p class="text-sm text-gray-600 mb-4">{{ result.story }}</p>
              <div class="flex items-center justify-between">
                <span class="text-sm text-gray-500">Confidence: {{ (result.confidence * 100).toFixed(2) }}%</span>
                <div class="flex items-center">
                  <span class="inline-block w-3 h-3 bg-green-500 rounded-full mr-2"></span>
                  <span class="text-sm text-gray-500">Classified</span>
                </div>
              </div>
            </div>
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
const audioFile = ref(null);
const isSubmitting = ref(false);
const loading = ref(false);
const results = ref([]);
const errorMessage = ref('');

const handleFileChange = (event) => {
  audioFile.value = event.target.files[0];
  errorMessage.value = '';
};

const handleSubmit = async () => {
  if (!audioFile.value) {
    errorMessage.value = 'Please upload a valid audio file.';
    return;
  }

  isSubmitting.value = true;
  loading.value = true;

  const formData = new FormData();
  formData.append('audio', audioFile.value);

  axios.post('http://localhost:5000/api/predict', formData, {
    headers: {
      'Content-Type': 'multipart/form-data'
    }
  }).then((response) => {
    results.value = response.data.results;
    loading.value = false;
    isSubmitting.value = false;
    
  }).catch((error) => {
    errorMessage.value = error.response.data.message;
    loading.value = false;
    
    isSubmitting.value = false;
  });
 
};
</script>

<style scoped>
/* Animations */
@keyframes fadeIn {
  0% {
    opacity: 0;
  }

  100% {
    opacity: 1;
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 1s ease;
}

.fade-enter,
.fade-leave-to {
  opacity: 0;
}

/* Custom styling */
.bg-gradient-to-r {
  background: linear-gradient(135deg, #4f83cc, #6c7dff);
}

.transform:hover {
  transform: translateY(-5px);
}

.transition-all {
  transition: all 0.3s ease-in-out;
}

.card {
  transition: transform 0.3s, box-shadow 0.3s;
}

.card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}
</style>
