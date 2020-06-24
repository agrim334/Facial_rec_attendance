<template>
  <div class="home">
    <AddDeptForm @deptadd="validate">
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
    validate(newdept) {
      console.log(newdept);
      if (newdept.id === null || newdept.id === '') {
        alert('Fill in id');
      }
      if (newdept.name === null || newdept.name === '') {
        alert('Fill in name');
      }
      this.add(newdept);
    },
    add(data) {
      const path = 'http://localhost:5000/dept/add_dept_json';
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
