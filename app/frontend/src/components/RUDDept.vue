<template>
 <div>
    {{ course.id }}
    {{ course.coursename }}
    <button @click="deleterec"> Delete </button>
    <button @click="updaterec"> Update </button>
 </div>
</template>

<script>
export default {
  name: 'deptrec',
  props: { dept: Array },
  methods: {
    updaterec() {
      this.$emit('updrec', this.dept);
    },
    deleterec() {
      this.$emit('delrec', this.dept);
    },
  },
};
</script>
