<template>
  <div class="home">
    <table>
      <tr v-for='map in maps' :key='map.uid'>
        <MapRecord :map='map' @updrec='updaterec' @delrec='deleterec'></MapRecord>
      </tr>
    </table>
    <button id='add' @click='addrec'>Add maps</button>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import MapRecord from '@/components/RUDMap.vue';

export default {
  name: 'MapTable',
  props: {
    maps: Array,
  },
  components: {
    MapRecord,
  },
  methods: {
    updaterec(mapdat) {
      alert(mapdat);
    },
    deleterec(mapdat) {
      alert(mapdat);
    },
    addrec() {
      alert('sdcf');
    },
    getMaps() {
      const path = 'http://localhost:5000/map/check_map_json';
      axios.get(path)
        .then((res) => {
          this.maps = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getMaps();
  },
};
</script>
