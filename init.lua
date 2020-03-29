local http = minetest.request_http_api()

minetest.register_globalstep(function(dtime)

	http.fetch({
		url = 'http://localhost:2468/code/get'
	}, function(resp)
		local payload = minetest.parse_json(resp.data)
		if payload then
			local response = {}
			for i = 1, #payload do
				local res = {id = payload[i].id}
				local succ, value = eval(payload[i].code)
				if succ then 
					res['value'] = dump(value)
				else
					res['error'] = value 
				end
				table.insert(response, res)
			end 

			http.fetch({
				url = 'http://localhost:2468/response/add',
				post_data = minetest.write_json(response)
			}, function(resp) end)
		end
	end)

end)

function errhandler(e)
	-- TODO collect errors
	minetest.debug('reploops' .. dump(e))
end

function eval(s)
	minetest.debug('calling ' .. s)
	local fn = loadstring(s)
	return pcall(fn)
end
