<template>
  <div class="home">
    <AddMapForm @mapadd='add' @imgupl='imgupl' :isstud='isstud'>
    </AddMapForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import AddMapForm from '@/components/AddMap.vue';

export default {
  name: 'AddMap',
  components: {
    AddMapForm,
  },
  data() {
    return {
      isstud: 0,
      cid: -1,
    };
  },
  methods: {
    add(data) {
      const path = 'http://localhost:5000/map/add_map_json';
      const updat = data;
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then((res) => {
          this.isstud = res.data.isstud;
          this.cid = data.cid;
          if (this.isstud === 0) alert('Success in adding map');
        })
        .catch((error) => {
          console.error(error);
        });
    },
    imgupl(data) {
      const path = 'http://localhost:5000/map/add_map_json';
      const formData = new FormData();
      formData.append('file', data.img);
      formData.append('uid', data.dat.uid);
      formData.append('cid', data.dat.cid);
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
