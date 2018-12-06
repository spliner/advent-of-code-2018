defmodule Point do
    @enforce_keys [:x, :y]
    defstruct [:x, :y] 
end

defmodule Rectangle do
    @enforce_keys [:p1, :p2]
    defstruct [:p1, :p2] 
end

defmodule Claim do
    @enforce_keys [:id, :bounds]
    defstruct [:id, :bounds] 
end

defmodule Day3 do
    def part1(path, regex) do
        lines = read_file(path, regex)

        lines
        |> Enum.with_index()
        |> Enum.reduce(MapSet.new(), fn {x, i}, acc ->
            points = lines
                |> Enum.drop(i + 1)
                |> Enum.map(fn y -> calculate_intersection(x.bounds, y.bounds) end)
                |> Enum.filter(fn i -> !!i end)
                |> Enum.map(fn i -> get_all_points(i) end)
                |> List.flatten()
            MapSet.union(acc, MapSet.new(points))
        end)
        |> MapSet.size()
        |> IO.inspect()
    end

    defp read_file(path, regex) do
        path
        |> File.read!()
        |> String.split("\r\n", trim: true)
        |> Enum.map(fn l -> parse_line(l, regex) end)
    end

    defp parse_line(line, regex) when is_binary(line) do
        matches = Regex.named_captures(regex, line)
        |> Enum.map(fn {k, v} -> {String.to_atom(k), String.to_integer(v)} end)
        |> Enum.into(%{})

        p1 = %Point{x: matches.x, y: matches.y}
        p2 = %Point{x: matches.x + matches.w - 1, y: matches.y + matches.h - 1}
        %Claim{id: matches.id, bounds: %Rectangle{p1: p1, p2: p2}}
    end

    defp calculate_intersection(rectangle1, rectangle2) when is_map(rectangle1) and is_map(rectangle2) do
        x1 = Enum.max([rectangle1.p1.x, rectangle2.p1.x])
        y1 = Enum.max([rectangle1.p1.y, rectangle2.p1.y])
        x2 = Enum.min([rectangle1.p2.x, rectangle2.p2.x])
        y2 = Enum.min([rectangle1.p2.y, rectangle2.p2.y])
        is_valid = x1 <= x2 and y1 <= y2
        if is_valid do
            p1 = %Point{x: x1, y: y1}
            p2 = %Point{x: x2, y: y2}
            %Rectangle{p1: p1, p2: p2}
        else
            nil
        end
    end

    defp get_all_points(rectangle) when is_map(rectangle) do
        x_range = rectangle.p1.x..rectangle.p2.x
        y_range = rectangle.p1.y..rectangle.p2.y

        x_range
        |> Enum.map(fn x -> Enum.map(y_range, fn y -> {x, y} end) end)
        |> List.flatten()
    end

    def part2(path, regex) do
        lines = read_file(path, regex)
        
        intersected_ids = lines
            |> Enum.with_index()
            |> Enum.reduce(MapSet.new(), fn {x, i}, acc ->
                ids = lines
                    |> Enum.drop(i + 1)
                    |> Enum.filter(fn y -> !!calculate_intersection(x.bounds, y.bounds) end)
                    |> List.foldl(MapSet.new(), fn y, acc -> MapSet.put(acc, y.id) end)

                acc = 
                    if MapSet.size(ids) > 0 do
                        MapSet.put(acc, x.id)
                    else
                        acc
                    end
                MapSet.union(acc, ids)
            end)
        
        claim = lines |> Enum.find(fn l -> !MapSet.member?(intersected_ids, l.id) end)
        IO.inspect(claim.id)
    end
end
regex = ~r/#(?<id>\d+)\s@\s(?<x>\d+),(?<y>\d+):\s(?<w>\d+)x(?<h>\d+)/
test_path = "../inputs/day3_test.txt"
path = "../inputs/day3.txt"

Day3.part1(test_path, regex)
Day3.part1(path, regex)

Day3.part2(test_path, regex)
Day3.part2(path, regex)