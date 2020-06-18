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
  name: 'courserec',
  props: { course: Array },
  methods: {
    updaterec() {
      this.$emit('updrec', this.course);
    },
    deleterec() {
      this.$emit('delrec', this.course);
    },
  },
};
</script>
