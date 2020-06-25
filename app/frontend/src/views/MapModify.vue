<template>
  <div class="home">
    <ModifyMapForm :ogmap = 'map' @mapupd='updaterec'>
    </ModifyMapForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ModifyMapForm from '@/components/ModifyMap.vue';

export default {
  name: 'MapModify',
  props: {
    map: Array,
  },
  components: {
    ModifyMapForm,
  },
  methods: {
    updaterec(mapdat) {
      const path = 'http://localhost:5000/map/modify_map_json';
      axios.post(path, { old: this.map, new: mapdat })
        .then(() => {
          console.log('done');
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
