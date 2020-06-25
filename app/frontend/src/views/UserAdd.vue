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
      const path = 'http://localhost:5000/dept/check_dept_json';
      axios.get(path)
        .then((res) => {
          this.depts = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    getRole() {
      const path = 'http://localhost:5000/roles/check_role_json';
      axios.get(path)
        .then((res) => {
          this.roles = res.data.records;
        })
        .catch((error) => {
          console.error(error);
        });
    },
    add(data) {
      const path = 'http://localhost:5000/users/add_log_json';
      axios.post(path, data)
        .then((res) => {
          alert(res.data);
        })
        .catch((error) => {
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
