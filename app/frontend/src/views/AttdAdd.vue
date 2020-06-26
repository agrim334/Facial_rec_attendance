<template>
  <div class="home">
    <MarkAttdFaceForm @attdmark='addface'> </MarkAttdFaceForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import MarkAttdFaceForm from '@/components/AddAttdFaceRec.vue';

export default {
  name: 'AddAttdFace',
  props: { studlist: Array },
  components: {
    MarkAttdFaceForm,
  },
  methods: {
    addface(data) {
      const path = 'http://localhost:5000/attd/add_attd_json';
      axios.post(path, data.rec)
        .then((res) => {
          alert(res.data);
        })
        .catch((error) => {
          console.error(error);
        });
      const formData = new FormData();
      for (let i = 0; i < data.img.length; i += 1) {
        const tfile = data.img[i];
        formData.append('files['.concat(i).concat(']'), tfile);
      }
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
