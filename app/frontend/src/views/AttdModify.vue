<template>
  <div class="home">
    <ModifyAttdForm :attdrec = 'attd' @attdupd='updaterec'> </ModifyAttdForm>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ModifyAttdForm from '@/components/ModifyAttd.vue';

export default {
  name: 'attdModify',
  props: {
    attd: Array,
  },
  components: {
    ModifyAttdForm,
  },
  methods: {
    logout() {
      this.$store.dispatch('logout')
        .then(() => this.$router.push('/login'));
    },
    updaterec(modattd) {
      const path = 'attd/modify_attd_json';
      const updat = { old: this.attd, new: modattd };
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then((response) => {
          alert(response.data.result);
          console.log(response);
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
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
