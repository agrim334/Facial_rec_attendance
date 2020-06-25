<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>Department ID</label>
    <input type="text" placeholder = "Enter Department ID" v-model = 'dept.id' />
    <br>

    <label>Department name</label>
    <input type="text" placeholder = "Enter Department Name" v-model = 'dept.name' />
    <br>

    <input type="submit" value="Add deptartment" />
    </form>
  </div>
</template>

<script>
export default {
  name: 'AddDeptForm',
  data() {
    return {
      dept: {
        id: '', name: '',
      },
    };
  },
  methods: {
    handle() {
      let f = 0;
      if (this.dept.id === null || this.dept.id === '') {
        alert('fill dept id');
        f = 1;
      }
      if (this.dept.name === null || this.dept.name === '') {
        alert('fill dept name');
        f = 1;
      }
      if (f === 0) {
        this.$emit('deptadd', this.dept);
      }
    },
  },
};
</script>
