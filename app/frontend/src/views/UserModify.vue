<template>
  <div class="home">
    <ModifyUser :userrec = 'user' :depts = 'depts' :roles = 'roles'
    @userupd='updaterec'> </ModifyUser>
  </div>

</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import ModifyUser from '@/components/ModifyUser.vue';

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
      axios.post(path, { old: this.user, new: userdat })
        .then(() => {
          console.log(this);
        })
        .catch((error) => {
          console.error(error);
        });
    },
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
  },
  created() {
    this.getDept();
  },

};
</script>
