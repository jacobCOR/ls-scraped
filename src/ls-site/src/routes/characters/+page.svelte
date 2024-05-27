<script>
    export let data;
    console.log('char_name in component:', data);
</script>

<h1>
    Characters
</h1>
<p>
    {data.props.char_name}
</p>
