<template>
 <div>
    <input type='checkbox' :value = 'stud.id'>
 </div>
</template>

<script>
export default {
  name: 'ManAttdList',
  props: { stud: Array },
};
</script>
