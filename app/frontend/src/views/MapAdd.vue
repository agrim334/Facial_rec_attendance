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
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    add(data) {
      if (this.$store.getters.isAuthenticated) {
        const path = 'map/add_map_json';
        const updat = data;
        this.$store.dispatch('authrequest', { url: path, data: updat })
          .then((response) => {
            alert(response.data.result);
            console.log(response);
            this.isstud = response.data.isstud;
            this.cid = data.cid;
            if (this.isstud === 0) alert('Success in adding map');
          })
          .catch((error) => {
            alert(error.response.data.result);
            console.error(error);
          });
      }
      else {
        alert("Session expired. You have to login again");
        this.logout();
      }
    },
    imgupl(data) {
      if (this.$store.getters.isAuthenticated) {
        const path = 'map/add_map_json';
        const formData = new FormData();
        formData.append('file', data.img);
        formData.append('uid', data.dat.uid);
        formData.append('cid', data.dat.cid);
        this.$store.dispatch('authrequestimg', { url: path, data: formData })
          .then((response) => {
            alert(response.data.result);
            console.log(response);
          })
          .catch((error) => {
            alert(error.response.data.result);
            console.error(error);
          });
      }
      else {
        alert("Session expired. You have to login again");
        this.logout();
      }
    },
  },
  created() {
    if (!this.$store.getters.isAuthenticated) {
      alert("Session expired. You have to login again");
      this.logout();
    }
  },
};
</script>
