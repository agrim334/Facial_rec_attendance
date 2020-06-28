<template>
  <div class="home">
    <label>Filters</label>
    <br>
    <input type='radio' id='PC' value='1' v-model = 'choice' @change='getMaps'>
    <label for='PC'> ProfCourses </label>
    <input type='radio' id='TC' value='2' v-model = 'choice' @change='getMaps'>
    <label for='TC'> TACourses </label>
    <input type='radio' id='SC' value='3' v-model = 'choice' @change='getMaps'>
    <label for='SC'> StudCourses </label>

    <MapRecord :maps='maps' @updrec='updaterec' @delrec='deleterec'>
    </MapRecord>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import MapRecord from '../components/RUDMap.vue';

export default {
  name: 'MapTable',
  props: {
    maps: Array,
  },
  components: {
    MapRecord,
  },
  data() {
    return {
      choice: '',
    };
  },
  methods: {
    updaterec(mapdat) {
      this.$router.push({ name: 'MapModify', params: { map: mapdat } });
    },
    deleterec(mapdat) {
      const path = 'http://localhost:5000/map/delete_map_json';
      axios.post(path, mapdat)
        .then((res) => {
          alert(res.data.status);
          this.getMaps();
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getMaps() {
      const path = 'http://localhost:5000/map/check_map_json';
      axios.post(path, this.choice)
        .then((res) => {
          const temp = res.data.records_t.concat(res.data.records_p);
          const t2 = res.data.records_s.concat(temp);
          this.maps = t2;
          for (let i = 0; i < this.maps.length; i += 1) {
            this.maps[i].actions = '';
          }
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
