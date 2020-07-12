<template>
  <div class="home">
    <RegisterForm @userreg="add" :roles="roles" :depts="depts">
    </RegisterForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import RegisterForm from '@/components/AddUser.vue';

export default {
  name: 'Reg',
  components: {
    RegisterForm,
  },
  data() {
    return {
      roles: Array,
      depts: Array,
    };
  },
  methods: {
    getDept() {
      const path = 'dept/check_dept_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((response) => {
          this.depts = response.data.records;
          console.log(this.depts);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getRole() {
      const path = 'roles/check_role_json';
      this.$store.dispatch('authrequest', { url: path, data: '' })
        .then((response) => {
          this.roles = response.data.records;
          console.log(this.roles);
        })
        .catch((error) => {
          console.error(error);
        });
    },
    add(data) {
      const path = 'users/add_log_json';
      const updat = data;
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
    this.getDept();
    this.getRole();
  },
};
</script>
