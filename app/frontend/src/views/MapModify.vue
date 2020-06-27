<template>
  <div class="home">
    <ModifyMapForm :ogmap = 'map' @mapupd='updaterec' @imgupl='imgupl' :isstud='isstud'>
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
  data() {
    return {
      isstud: { val: 0, uid: -1 },
    };
  },
  components: {
    ModifyMapForm,
  },
  methods: {
    updaterec(mapdat) {
      const path = 'http://localhost:5000/map/modify_map_json';
      axios.post(path, { old: this.map, new: mapdat })
        .then((res) => {
          console.log(res.data.status);
          this.isstud.val = res.data.isstud;
          this.isstud.uid = mapdat.uid;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    imgupl(data) {
      const path = 'http://localhost:5000/map/modify_map_json';
      const formData = new FormData();
      formData.append('file', data.img);
      formData.append('uid', this.isstud.uid);
      axios.post(path, formData, { headers: { 'Content-Type': 'multipart/form-data' } })
        .then((res) => {
          alert(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
};
</script>
