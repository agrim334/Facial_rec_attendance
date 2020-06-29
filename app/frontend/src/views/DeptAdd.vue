<template>
  <div class="home">
    <AddDeptForm @deptadd="add">
    </AddDeptForm>
  </div>
</template>

<script>
// @ is an alias to /src
import axios from 'axios';
import AddDeptForm from '@/components/AddDept.vue';

export default {
  name: 'AddDept',
  components: {
    AddDeptForm,
  },
  methods: {
    add(data) {
      const path = 'http://localhost:5000/dept/add_dept_json';
      const updat = data;
      this.$store.dispatch('authrequest', { url: path, data: updat })
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
