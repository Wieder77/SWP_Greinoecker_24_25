<script setup>
import { ref } from 'vue';
import axios from 'axios';

const searchResult = ref(null);
const searchWord = ref('');
const activeEditItem = ref(null); // Speichert das aktuell bearbeitete Item
const historyData = ref([]);


const getImageUrl = (thump) => {
  return 'https://webapp.uibk.ac.at/ubi/cat/' + thump;
};

const fetchData = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:5000/cat-search/' + searchWord.value);
    searchResult.value = response.data;
  } catch (error) {
    console.error('Error fetching data:', error);
    searchResult.value = { error: 'Unable to fetch data' };
  }
};

const saveItem = async (item) => {
  try {
    await axios.patch(`http://localhost:5000/cat-item/${item.id}`, {
      params: {
        description: item.description
      }
    });
    activeEditItem.value = null; // Nach dem Speichern die Anzeige zurücksetzen
  } catch (error) {
    console.error('Error saving item:', error);
  }
};
const addHistory = async (item) => {
  try {
    await axios.post(`http://127.0.0.1:5000/history/${item.id}`, {
      description: item.description
    });
    console.log('History gespeichert');
  } catch (error) {
    console.error('Fehler beim Speichern in History:', error);
  }
};

const loadHistory = async (item) => {
  try {
    const response = await axios.get(`http://127.0.0.1:5000/history/${item.id}`);
    historyData.value = response.data;
  } catch (error) {
    console.error('Error loading history:', error);
  }
};
</script>

<template>
  <div class="container">
    <form @submit.prevent="fetchData" class="search-form">
      <input type="text" v-model="searchWord" placeholder="Search.." name="search" class="search-input">
      <button type="submit" class="button">Search</button>
    </form>

    <!-- Anzeige des aktuellen Bearbeitungsfeldes -->
    <div v-if="activeEditItem" class="active-label">
      Aktuell bearbeitetes Feld: <strong>ID {{ activeEditItem.id }}</strong>
    </div>

    <div v-if="searchResult" class="search-result">
      <div v-for="item in searchResult" :key="item.id" class="result-row">
        <div class="text-box">
            <textarea v-model="item.description" rows="10" cols="50"></textarea>
            <!-- Hier wird die History angezeigt -->
            <div v-if="activeEditItem && activeEditItem.id === item.id && historyData.length > 0" class="history-box">
              <h4>Änderungsverlauf:</h4>
              <p style="font-size: 0.9em; color: #666;">Klicke auf einen alten Text, um ihn wiederherzustellen:</p>
              <ul>
                <li 
                  v-for="entry in historyData" 
                  :key="entry.id" 
                  @click="item.description = entry.description"
                  style="cursor: pointer; padding: 6px; border-bottom: 1px solid #ddd;"
                >
                  <strong>{{ new Date(entry.change_date).toLocaleString() }}:</strong> {{ entry.description }}
                </li>
              </ul>
            </div>

            <!-- Buttons -->
            <button class="edit-button" @click="() => {
              activeEditItem = item;
              saveItem(item);
              addHistory(item);
            }">Speichern</button> 

            <button class="edit-button" @click="() => {
              activeEditItem = item;
              loadHistory(item);
            }">Show History</button>
          </div>
        <div class="image-box">
          <img :src="getImageUrl(item.thumb)" alt="Bild" class="preview-image" />
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.active-label {
  font-size: 18px;
  margin-bottom: 20px;
  color: #555;
}

.edit-button {
  margin-top: 15px;
  padding: 10px 20px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
}

.search-result {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.container {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 50px;
  padding: 0 20px;
  width: 100%;
  box-sizing: border-box;
}

.search-form {
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 30px;
}

.search-input {
  width: 500px;
  max-width: 100%;
  height: 50px;
  padding: 10px;
  font-size: 18px;
  border: 2px solid #ccc;
  border-radius: 5px;
}

.search-input:focus {
  border-color: #000;
  outline: none;
}

.button {
  padding: 15px 30px;
  background-color: #000;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
}

.button:hover {
  background-color: #333;
}

.result-row {
  display: flex;
  width: 100%;
  max-width: 1000px;
  margin: 0 auto 40px auto;
  box-sizing: border-box;
}

.image-box {
  width: 50%;
  height: auto;
  display: flex;
  justify-content: center;
  align-items: center;
}

.preview-image {
  max-width: 100%;
  max-height: 100%;
  object-fit: contain;
}
</style>
