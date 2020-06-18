<template>
  <div id="register-form">
    <form @submit.prevent="handle">
    <label>Department ID</label>
    <input type="text" placeholder = "Enter Department ID" v-model = 'dept.did' />
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
        did: '', name: '',
      },
    };
  },
  methods: {
    handle() {
      this.$emit('deptadd', this.dept);
    },
  },
};
</script>
