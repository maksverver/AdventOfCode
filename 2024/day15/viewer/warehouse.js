const exampleInput = `\
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
`;

// Global variables

const scale = 64;  // pixels
const moveSubdivison = 6;  // number of times to toggle move state per move
let moveDelay = getMoveDelay(document.getElementById('speed').value);  // milliseconds
let lastInput = exampleInput;
let lastPart2 = document.getElementById('part2').checked;
let runCount = 0;  // used to detect restarts in animateFrame()

function parseGridData(gridData, part2) {
    const grid_lines = gridData.trim().split('\n').map(line => line.trim());
    // positions[0] is the starting position of the warehouse keeper
    // positions[i..n] are the positions of the boxes
    const positions = [undefined];
    // grid[r][c] contains -1 for a wall, 0 for empty, or a positive box index
    const grid = [];
    for (let r = 0; r < grid_lines.length; ++   r) {
        const line = grid_lines[r];
        const row = [];
        for (const ch of line) {
            const c = row.length;
            switch (ch) {
                case '#':
                    row.push(-1);
                    if (part2) row.push(-1);
                    break;
                case '@':
                    if (positions[0] != null) {
                        throw new Error('Multiple starting locations ("@")');
                    }
                    positions[0] = {r, c};
                    // falls through
                case '.':
                    row.push(0);
                    if (part2) row.push(0);
                    break;
                case 'O':
                    row.push(positions.length);
                    positions.push({r, c});
                    if (part2) {
                        row.push(positions.length);
                        positions.push({r, c: c + 1});
                    }
                    break;
                default:
                    throw new Error(`Unrecognized character at position ${r}, ${c}: ${ch}`);
            }
        }
        grid.push(row);
    }
    if (positions[0] == null) {
        throw new Error('Missing starting location ("@")');
    }
    // Check that grid is enclosed in walls:
    const height = grid.length;
    const width = grid[0].length;
    for (let r = 0; r < height; ++r) {
        if (grid[r].length != width) {
            throw new Error('Grid has inconsistent width!');
        }
        if (grid[r][0] != -1 || grid[r][width - 1] != -1) {
            throw new Error('Grid is not enclosed in walls!');
        }
    }
    for (let c = 0; c < width; ++c) {
        if (grid[0][c] != -1 || grid[height - 1][c] != -1) {
            throw new Error('Grid is not enclosed in walls!');
        }
    }
    return [grid, positions];
}

function parseInput(text, part2) {
    const parts = text.split(/\r?\n\r?\n/);
    if (parts.length != 2) {
        throw new Error(`Incorrect number of parts ${parts.length}`);
    }

    const moves = parts[1].split(/\s+/).join('');
    const [grid, positions] = parseGridData(parts[0], part2);
    return [grid, positions, moves];
}

class Sprite {
    constructor(index, div, position, moveStates) {
        this.index = index;
        this.div = div;
        this.position = position;  // note this is actually mutable!
        this.moveDir = undefined;
        this.moveStates = moveStates || [];
    }

    moveTo(r, c) {
        this.div.style.top = `${r * scale}px`;
        this.div.style.left = `${c * scale}px`;
    }

    setMoveDir(moveDir) {
        if (this.moveDir) {
            this.div.classList.toggle(this.moveDir, false);
        }
        this.div.classList.toggle(moveDir, true);
        this.moveDir = moveDir;
    }

    clearAnimation() {
        for (const s of this.moveStates) {
            this.div.classList.remove(s);
        }
        const {r, c} = this.position;
        this.moveTo(r, c);
    }

    animateMove(dr, dc, offset) {
        this.moveTo(this.position.r + dr * offset, this.position.c + dc * offset);

        const states = this.moveStates;
        if (states.length > 0) {
            let activeIndex = Math.floor(offset * moveSubdivison) % states.length;
            if (activeIndex < 0) activeIndex += states.length;  // handle negative offset
            for (let i = 0; i < states.length; ++i) {
                this.div.classList.toggle(states[i], i == activeIndex);
            }
        }
    }
}

function restart(input) {
    const part2 = lastPart2;

    let parseResult;
    try {
        parseResult = parseInput(input ?? lastInput, part2);
    } catch (e) {
        console.error(e);
        alert(`Failed to parse input data: ${e.message}\n\nSee Javascript console for details.`);
        return;
    }
    if (input != null) lastInput = input;

    const [grid, positions, moves] = parseResult;
    const thisRun = ++runCount;

    const gridElem = document.getElementById('grid');
    gridElem.style.height = `${grid.length * scale}px`;
    gridElem.style.width = `${grid[0].length * scale}px`;

    function createSpriteDiv(type, r, c) {
        const div = document.createElement('div');
        div.classList.add('sprite', type);
        div.style.top = `${r * scale}px`;
        div.style.left = `${c * scale}px`;
        gridElem.appendChild(div);
        return div;
    }

    gridElem.replaceChildren();
    for (let r = 0; r < grid.length; ++r) {
        for (let c = 0; c < grid[r].length; ++c) {
            if (grid[r][c] == -1) {
                createSpriteDiv('wall', r, c);
            }
        }
    }
    const sprites = [];
    for (let i = 0; i < positions.length; ++i) {
        const pos = positions[i];
        if (i === 0) {
            const div = createSpriteDiv('player', pos.r, pos.c);
            sprites.push(new Sprite(i, div, pos, ['move-1', 'move-2']));
        } else {
            const div = createSpriteDiv('crate', pos.r, pos.c);
            if (part2) div.classList.add(pos.c % 2 === 0 ? 'left' : 'right');
            sprites.push(new Sprite(i, div, pos));
        }
    }

    const movesElem = document.getElementById('moves');
    const moveElems = [];
    for (let i = 0; i < moves.length; ++i) {
        const span = document.createElement('span');
        span.classList.add('move');
        span.appendChild(document.createTextNode(moves.charAt(i)));
        moveElems.push(span);
    }
    movesElem.replaceChildren(...moveElems);

    function recalculateAnswer(part2) {
        let answer = 0;
        for (let i = 1; i < positions.length; i += part2 ? 2 : 1) {
            const {r, c} = positions[i];
            answer += 100*r + c;
        }
        return answer;
    }

    function updateAnswer(part2) {
        answerElem.textContent = recalculateAnswer(part2);
    }

    const answerElem = document.getElementById('answer');
    updateAnswer(lastPart2);

    function other(i) {
        if (i <= 0) throw new Error(`Invalid box index ${i}`);
        return (i & 1) ? i + 1 : i - 1;
    }

    // Returns a list of indices of boxes to push, or an empty list if there are none,
    // or undefined if the player cannot move into that direction.
    function calculateMove(r, c, dr, dc) {
        r += dr;
        c += dc;
        const i = grid[r][c];
        if (i === 0) return [];  // Free space. Just walk.
        if (i < 0) return undefined;  // Blocked by a wall!
        const queue = [i];
        if (part2) queue.push(other(i));        
        const added = new Set(queue);
        for (let queue_pos = 0; queue_pos < queue.length; ++queue_pos) {
            const i = queue[queue_pos];
            let {r, c} = positions[i];
            r += dr;
            c += dc;
            const j = grid[r][c];
            if (j < 0) return undefined;  // Blocked by a wall!
            if (j > 0 && !added.has(j)) {
                added.add(j);
                queue.push(j);
                if (part2) {
                    const k = other(j)
                    added.add(k);
                    queue.push(k);
                }
            }
        }
        return queue;
    }

    function runAnimation() {
        let lastTimestamp = undefined;
        let moveIndex = 0;

        let movingSprites = [];
        let moveDr = 0, moveDc = 0;

        function startNewMove() {
            if (moveIndex >= moves.length) {
                return false;
            }

            moveElems[moveIndex].classList.add('current');

            // Decode next move.
            let dr = 0, dc = 0, moveDir;
            switch (moves.charAt(moveIndex)) {
                case '^': dr = -1; moveDir = 'up';    break;
                case 'v': dr = +1; moveDir = 'down';  break;
                case '<': dc = -1; moveDir = 'left';  break;
                case '>': dc = +1; moveDir = 'right'; break;
                default:
                    alert('Invalid move character at index ' + moveIndex + ': ' + moves.charAt(moveIndex));
                    throw new Error('Invalid move');
            }
            moveIndex += 1;

            // This is just for animation.
            sprites[0].setMoveDir(moveDir);

            // Figure out which sprites to move
            const {r, c} = sprites[0].position;
            const crates = calculateMove(r, c, dr, dc);
            moveElems[moveIndex - 1].classList.add(
                crates == null ? 'failed' :
                crates.length == 0 ? 'moved' : 'pushed');
            if (crates == null) {
                // Can't move in that direction. I could do movingSprites = [] 
                // but this way, we can see the player trying to move in the animation:
                movingSprites = [sprites[0]];
                moveDr = 0;
                moveDc = 0;
            } else {
                // Prepare animation state.
                movingSprites = [0, ...crates].map((i) => sprites[i]);
                moveDr = dr;
                moveDc = dc;
                // Move player.
                positions[0].r += dr;
                positions[0].c += dc;
                // Move crates.
                for (let i of crates) {
                    const {r, c} = positions[i];
                    grid[r][c] = 0;
                }
                for (let i of crates) {
                    let {r, c} = positions[i];
                    r += dr;
                    c += dc;
                    grid[r][c] = i;
                    positions[i].r = r;
                    positions[i].c = c;
                }
            }
            updateAnswer(part2);
            return true;
        }

        function animateCurrentMove(offset) {
            for (const sprite of movingSprites) {
                sprite.animateMove(moveDr, moveDc, offset);
            }
        }

        function finishCurrentMove() {
            moveElems[moveIndex - 1].classList.remove('current');
            for (const sprite of movingSprites) {
                sprite.clearAnimation();
            }
            movingSprites = [];
            moveDr = 0;
            moveDc = 0;
        }

        function animateFrame(timestamp) {
            if (thisRun != runCount) return;  // we have restarted! end the animation
            if (lastTimestamp == null) {
                lastTimestamp = timestamp;
                if (!startNewMove()) return;  // this ends the animation
            } else {
                let offset = (timestamp - lastTimestamp) / moveDelay;
                while (offset >= 1) {
                    lastTimestamp += moveDelay;
                    offset -= 1;
                    finishCurrentMove();
                    if (!startNewMove()) return;  // this ends the animation
                }
                animateCurrentMove(offset - 1);
            }
            requestAnimationFrame(animateFrame);
        }

        requestAnimationFrame(animateFrame);    
    }

    runAnimation();
}

function handleLoad() {
    // Start animation only after resources are loaded.
    //
    // This should prevent image flickering due to CSS background images
    // not being loaded yet.
    restart();
}

function handleOpenFile(target) {
    let file = target.files[0];
    if (file == null) return;  // nothing selected

    var reader = new FileReader();
    reader.onload = (e) => restart(e.target.result);
    reader.readAsText(file);
}

function getMoveDelay(value) {
    return value <= 0 ? Infinity : (5000 >> value);
}

function handleSpeedChange(value) {
    moveDelay = getMoveDelay(value);
}

function handlePart2Change(value) {
    if (value != lastPart2) {
        lastPart2 = value;
        restart();
    }
}