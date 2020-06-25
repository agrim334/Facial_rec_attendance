<template>
  <div class="home">
    <table>
      <tr v-for='map in maps' :key='map.id'>
        <MapRecord :map='map' @updrec='updaterec' @delrec='deleterec'></MapRecord>
      </tr>
    </table>
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
      this.$router.push({ name: 'MapModify', params: { map: mapdat } });
    },
    deleterec(mapdat) {
      const path = 'http://localhost:5000/map/delete_map_json';
      axios.post(path, mapdat)
        .then(() => {
          this.getMaps();
        })
        .catch((error) => {
          console.error(error);
        });
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
