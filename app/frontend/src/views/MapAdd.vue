<template>
  <div class="home">
    <AddMapForm @mapadd='validate' @getusertype='getuser' >
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
  methods: {
    validate(newmap) {
      if (newmap.cid === null || newmap.cid === '') {
        alert('Enter CID');
      }
      if (newmap.uid === null || newmap.uid === '') {
        alert('Enter UID');
      }
      this.add(newmap);
    },
    add(data) {
      const path = 'http://localhost:5000/map/add_map_json';
      axios.post(path, data)
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
