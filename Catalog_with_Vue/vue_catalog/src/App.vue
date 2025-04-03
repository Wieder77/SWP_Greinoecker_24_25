<script setup>
import axios from 'axios'
const API_BASE_URL = 'http://127.0.0.1:5000';
/*
export const getCatalogItem = (id) => {
  return axios.get(`${API_BASE_URL}/cat-item/${id}`);
};
export const searchCatalog = (query) => {
  return axios.get(`${API_BASE_URL}/cat-search/${query}`);
};
*/
</script>
<template>
  <div class="search-container">
    <form action="/action_page.php" class="search-form">
      <input type="text" placeholder="Search.." name="search" class="search-input">
      <button type="submit" class="search-button">Submit</button>
    </form>
  </div>
</template>

<style scoped>
.search-container {
  display: flex;
  flex-direction: column;
  justify-content: flex-start; /* Positioniert den Inhalt oben */
  align-items: center; /* Zentriert den Inhalt horizontal */
  width: 100%; /* Nimmt die gesamte Breite ein */
  height: 100vh; /* Nimmt die gesamte Höhe des Bildschirms ein */
  padding-top: 20px; 
  box-sizing: border-box; 
}

.search-form {
  display: flex;
  width: 100%; /* Nimmt die gesamte Breite des Containers ein */
  max-width: 1200px; /* Optional: Begrenzung der Breite */
}

.search-input {
  flex-grow: 1;
  height: 50px; 
  font-size: 18px; 
  border: 2px solid #ccc; 
  border-radius: 5px 0 0 5px;
  padding-left: 10px;
  box-sizing: border-box; /* Für konsistente Größe */
}

.search-button {
  height: 50px; 
  font-size: 16px; 
  padding: 0 20px;
  background-color: #007BFF; 
  color: white;
  border: none;
  border-radius: 0 5px 5px 0;
  cursor: pointer;
}

.search-button:hover {
  background-color: #0056b3; /* Hover-Farbe */
}
</style>
