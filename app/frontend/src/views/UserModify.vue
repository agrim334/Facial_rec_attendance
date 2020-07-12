<template>
  <div class="home">
    <ModifyUser :userrec = 'user' :depts = 'depts' :roles = 'roles'
    @userupd='updaterec'> </ModifyUser>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ModifyUser from '../components/ModifyUser.vue';

export default {
  name: 'UserModify',
  props: {
    user: Object,
    depts: Array,
    roles: Array,
  },
  components: {
    ModifyUser,
  },
  methods: {
    updaterec(userdat) {
      const path = 'users/modify_log_json';
      const updat = { old: this.user, new: userdat };
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then((response) => {
          alert(response.data.result);
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
    },
    getDept() {
      const path = 'dept/check_dept_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((response) => {
          this.depts = response.data.records;
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
    },
    getRoles() {
      const path = 'roles/check_role_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((response) => {
          this.roles = response.data.records;
        })
        .catch((error) => {
          alert(error.response.data.result);
          console.error(error);
        });
    },
  },
  created() {
    this.getDept();
    this.getRoles();
  },

};
</script>
