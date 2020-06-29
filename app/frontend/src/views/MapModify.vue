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
      const updat = { old: this.map, new: mapdat };
      this.$store.dispatch('authrequest', { url: path, data: updat })
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
      this.$store.dispatch('authrequestimg', { url: path, data: formData })
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
