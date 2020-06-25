<template>
  <div class="home">
    <AddMapForm @mapadd='validate' :roles='roles' >
    </AddMapForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import AddMapForm from '@/components/AddMap.vue';

export default {
  name: 'AddMap',
  props: { roles: Array },
  components: {
    AddMapForm,
  },
  methods: {
    validate(newmap) {
      alert(newmap);
    },
    getroles() {
      const path = 'http://localhost:5000/roles/check_role_json';
      axios.get(path)
        .then((res) => {
          this.roles = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    this.getroles();
  },
};
</script>
