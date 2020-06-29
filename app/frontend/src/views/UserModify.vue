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
      const path = 'http://localhost:5000/users/modify_log_json';
      const updat = { old: this.user, new: userdat };
      this.$store.dispatch('authrequest', { url: path, data: updat })
        .then(() => {
          console.log(this);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getDept() {
      const path = 'http://localhost:5000/dept/check_dept_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((res) => {
          console.log(res.data);
          this.depts = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getRoles() {
      const path = 'http://localhost:5000/roles/check_role_json';
      axios.get(path)
        .then((res) => {
          console.log(res.data);
          this.roles = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
  },
  created() {
    console.log(this.user);
    this.getDept();
    this.getRoles();
  },

};
</script>
