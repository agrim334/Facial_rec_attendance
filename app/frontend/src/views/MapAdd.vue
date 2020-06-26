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
      isstud: { val: 0, uid: -1 },
    };
  },
  methods: {
    add(data) {
      const path = 'http://localhost:5000/map/add_map_json';
      axios.post(path, data)
        .then((res) => {
          this.isstud.val = res.data.isstud;
          this.isstud.uid = data.uid;
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
