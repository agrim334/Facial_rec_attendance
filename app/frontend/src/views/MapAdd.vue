<template>
  <div class="home">
    <AddMapForm @mapadd='add'>
    </AddMapForm>
    <form id="addimg" v-if='isstud === 1' @submit='uplimg'>
      <div >
        <label> Student Image </label>
        <input type="file" id="file" ref="file" accept="image/*" />
      </div>
      <input type="submit" value="Upload image" />
    </form>
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
      file: '',
    };
  },
  methods: {
    add(data) {
      const path = 'http://localhost:5000/map/add_map_json';
      axios.post(path, data)
        .then((res) => {
          this.isstud = res.data.isstud;
          if (this.isstud === 0) alert('Success in adding map');
        })
        .catch((error) => {
          console.error(error);
        });
    },
    uplimg() {
      const path = 'http://localhost:5000/map/add_map_json';
      console.log(this.$refs.file.file);
      this.file = this.$refs.file.file;
      const formData = new FormData();
      formData.append('file', this.file);
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
